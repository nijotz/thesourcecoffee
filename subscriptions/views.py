from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.conf import settings
from subscriptions.forms import SubscriptionForm
from subscriptions.models import Subscription

@login_required
@render_to('subscriptions/list.html')
def list(request):

    customer = request.user.customer

    # this will just show current subscription info without the form
    # I suppose I could have two templates, one with the info and one with
    # the form and return a different template based on the data, but I'm
    # just going to squeeze both into one template for now and split later
    # if need be.
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
