from annoying.decorators import render_to
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages import info, error
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from mezzanine.utils.urls import login_redirect
from customers.forms import CustomerForm
from customers.tests import signup_test_customer
from subscriptions.forms import SubscriptionForm
from subscriptions.models import Plan, Subscription


@user_passes_test(lambda u: u.is_superuser)
@login_required
def add_test_customer(request):
    signup_test_customer(request.POST)
    messages.info(request, 'Test customer added')
    return redirect(reverse('admin:index'))


@login_required
@render_to('customers/home.html')
def home(request):
    return locals()


@render_to('customers/signup.html')
def signup(request):

    stripe_key = settings.STRIPE_PUBLIC_KEY

    subscription_form = SubscriptionForm(request.POST or None)
    customer_form = CustomerForm(request.POST or None)

    # get plan prices in a jsonifiable format
    plans = Plan.objects.jsonify_for_form()

    context = {
        'customer_form': customer_form,
        'subscription_form': subscription_form,
        'stripe_key': stripe_key,
        'plans': plans
    }

    if not (request.method == "POST" and subscription_form.is_valid() and
        customer_form.is_valid()):
        return context

    with transaction.commit_on_success():
        save = transaction.savepoint()
        try:
            customer = customer_form.save(commit=False).customer
            customer.update_card(request.POST['stripeToken'])
            customer.save()

            if subscription_form.is_valid():
                plan = Plan.objects.get(
                    amount=subscription_form.cleaned_data['amount'],
                    interval=subscription_form.cleaned_data['interval'])
                subscription = Subscription(
                    customer=customer,
                    plan=plan)
                subscription.save()

            transaction.savepoint_commit(save)

            if not customer.user.is_active:
                send_verification_mail(request, customer.user, "signup_verify")
                info(request, _("A verification email has been sent with "
                                "a link for activating your account."))
                return redirect(request.GET.get("next", "/"))
            else:
                info(request, _("Successfully signed up"))
                auth_login(request, customer.user)
                return login_redirect(request)

        except Exception as e:
            error(request, e)
            transaction.savepoint_rollback(save)

    return context
