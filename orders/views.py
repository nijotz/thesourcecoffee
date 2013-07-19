from datetime import date, timedelta
from io import BytesIO
from annoying.decorators import render_to
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
import xhtml2pdf.pisa
from base.models import SiteSetting
from customers.models import Customer
from orders.models import MailOrder, Order


@login_required
@render_to('orders/list.html')
def list(request):
    orders = request.user.customer.orders
    fulfilled_orders = orders.exclude(fulfilled=None)
    next_order = orders.filter(fulfilled=None).order_by('to_be_fulfilled')[0]
    return locals()


@user_passes_test(lambda u: u.is_superuser)
@login_required
@render_to('orders/fulfillment.html')
def fulfillment(request):

    maximum = SiteSetting.objects.get(key='orders.max_fulfillment_day').value

    if request.POST:
        order = Order.objects.get(id=request.POST.get('order_id'))
        if not order.fulfilled:
            order.fulfill(tracking_number=request.POST.get('tracking_number'))
            order.customer.make_sure_rewards_have_orders()

        else:
            messages.warning(request, 'Order already fulfilled')

    unfilled_orders = Order.objects.filter(to_be_fulfilled__lte=date.today())
    unfilled_orders.order_by('to_be_fulfilled')

    # Limit to what can be fulfilled per day
    total = 0
    orders = []
    for order in unfilled_orders:

        # Filter out orders that are for a paused subscription
        if not order.subscription.active:
            continue

        amount = order.subscription.plan.amount
        if total + amount < maximum:
            orders.append(order)
            total += amount

    return locals()


@user_passes_test(lambda u: u.is_superuser)
@login_required
def mailing_stickers(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mailingstickers.pdf"'

    buffer = BytesIO()

    orders = MailOrder.objects.filter(to_be_fulfilled__lte=date.today()).select_related('customer')
    customers = [ o.customer for o in orders ]

    html = render(request, 'orders/mailing_stickers.html', locals())
    xhtml2pdf.pisa.CreatePDF(html.content, buffer)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


@user_passes_test(lambda u: u.is_superuser)
@login_required
def move_orders_back(request):

    days = int(request.REQUEST.get('days')) or 1

    def modify_time(obj, field):
        new_time = getattr(obj, field, None)
        if new_time:
            new_time -= timedelta(days=days)
            setattr(obj, field, new_time)
            obj.save()

    order_fields = ['to_be_fulfilled', 'fulfilled']
    for order in Order.objects.all():
        for field in order_fields:
            modify_time(order, field)

    messages.info(request, 'Orders moved backed in time {} day'.format(days))
    return redirect(reverse('admin:index'))
