from django.conf import settings
from django.contrib.auth import (authenticate, login as auth_login,
                                               logout as auth_logout)
from django.contrib.messages import info, error
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from customers.forms import CustomerForm
from subscriptions.forms import SubscriptionForm
from mezzanine.utils.views import render
from mezzanine.utils.urls import login_redirect


def signup(request, template="customers/account_signup.html"):

    stripe_key = settings.STRIPE_PUBLIC_KEY

    subscription_form = SubscriptionForm(request.POST or None)
    customer_form = CustomerForm(request.POST or None)

    if request.method == "POST" and subscription_form.is_valid() and \
        customer_form.is_valid():

        with transaction.commit_on_success():
            save = transaction.savepoint()
            try:
                customer = customer_form.save(commit=False)
                customer.update_card(request.POST['stripeToken'])
                subscription = subscription_form.save(commit=False)
                subscription.customer = customer
                customer.save()
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

    context = {
        'customer_form': customer_form,
        'subscription_form': subscription_form,
        'stripe_key': stripe_key,
    }

    return render(request, template, context)
