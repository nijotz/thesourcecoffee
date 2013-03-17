from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from subscriptions.forms import CustomerSubscriptionForm

@login_required
@render_to('subscriptions/list.html')
def list(request):

    customer = request.user.customer
    customer_subscription = customer.subscriptions.active()

    # this will just show current subscription info without the form
    # I suppose I could have two templates, one with the info and one with
    # the form and return a different template based on the data, but I'm
    # just going to squeeze both into one template for now and split later
    # if need be.
    if customer_subscription:
        return locals()

    msg = ''
    if request.method == 'POST':
        form = CustomerSubscriptionForm(customer, request.POST)
        if form.is_valid():
            customer_subscription = form.save(commit=False)
            customer_subscription.customer = customer
            customer_subscription.save()
            del form

    else:
        form = CustomerSubscriptionForm(customer)

    return locals()
