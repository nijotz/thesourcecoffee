from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from subscriptions.forms import CustomerSubscriptionForm

@login_required
@render_to('subscriptions/list.html')
def list(request):

    subscription = request.user.customer.subscriptions.all()

    if subscription:
        subscription = subscription[0]
    else:
        subscription = None

    form = CustomerSubscriptionForm(instance=subscription)

    return locals()
