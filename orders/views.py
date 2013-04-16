from datetime import date
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from orders.models import Order


@login_required
@render_to('orders/list.html')
def list(request):
    orders = request.user.customer.orders.all()
    return locals()


@user_passes_test(lambda u: u.is_superuser)
@login_required
@render_to('orders/fulfillment.html')
def fulfillment(request):
    orders = Order.objects.filter(to_be_fulfilled__lte=date.today())
    return locals()
