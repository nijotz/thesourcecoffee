from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from subscriptions.forms import SubscriptionForm
from subscriptions.models import Plan, Subscription

@login_required
@render_to('subscriptions/index.html')
def index(request):

    customer = request.user.customer

    try:
        subscription = customer.subscription
    except Subscription.DoesNotExist:
        subscription = None

    msg = ''

    if request.method == 'POST' and subscription:
        action = request.POST.get('action')
        if action == 'pause':
            subscription.pause()
        if action == 'unpause':
            subscription.unpause()
        #TODO
        #elif action == 'cancel':
        #    subscription.cancel()
        elif action == 'change':
            return HttpResponseRedirect(reverse('subscriptions.views.update'))

    return locals()


@login_required
@render_to('subscriptions/update.html')
def update(request):

    customer = request.user.customer
    plans = Plan.objects.jsonify_for_form()
    data_key = settings.STRIPE_PUBLIC_KEY

    subscription_form = None
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            plan = Plan.objects.get(
                amount=subscription_form.cleaned_data['amount'],
                interval=subscription_form.cleaned_data['interval'])
            customer.update_card(request.POST.get('stripeToken'))
            customer.subscription.plan = plan
            customer.subscription.save()
            # This fixes the bug where, when the form was submitted, the values
            # were unicode strings instead of ints and radio checking in the
            # template would not work because of type mismatch
            subscription_form = None

    if not subscription_form:
        subscription = customer.subscription
        subscription_form = SubscriptionForm({
            'amount':subscription.plan.amount,
            'interval':subscription.plan.interval})

    return locals()
