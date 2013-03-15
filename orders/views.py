from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required

@login_required
@render_to('orders/list.html')
def list(request):
    orders = request.user.customer.orders.all().select_subclasses()
    return locals()
