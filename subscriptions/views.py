from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from subscriptions.forms import CustomerSubscriptionForm

@login_required
@render_to('subscriptions/list.html')
def list(request):

    customer = request.user.customer

    subscription = customer.subscriptions.all()
    if subscription:
        subscription = subscription[0]
    else:
        subscription = None

    msg = ''
    if request.method == 'POST':
        form = CustomerSubscriptionForm(customer, request.POST, instance=subscription)
        if form.is_valid():
            cust_sub = form.save(commit=False)
            cust_sub.customer = customer
            cust_sub.save()
            msg = 'Subscription updated'

    else:
        form = CustomerSubscriptionForm(customer, instance=subscription)

    return locals()
