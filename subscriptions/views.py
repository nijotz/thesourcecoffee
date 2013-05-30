from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from subscriptions.forms import SubscriptionForm
from subscriptions.models import Subscription

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
        elif action == 'cancel':
            subscription.cancel()
        elif action == 'change':
            return HttpResponseRedirect(reverse('subscriptions.views.update'))

    return locals()


@login_required
@render_to('subscriptions/update.html')
def update(request):

    customer = request.user.customer

    try:
        subscription = customer.subscription
    except Subscription.DoesNotExist:
        subscription = None

    if subscription:
        return locals()

    msg = ''
    data_key = settings.STRIPE_PUBLIC_KEY

    if request.method == 'POST':
        form = SubscriptionForm(customer, request.POST)
        if form.is_valid():
            customer.update_card(request.POST.get('stripeToken'))
            customer.subscribe(
                form.cleaned_data['plan'],
                form.cleaned_data['location'])
            del form
    else:
        form = SubscriptionForm(customer)

    return locals()
