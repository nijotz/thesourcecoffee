from datetime import date
from io import BytesIO
from annoying.decorators import render_to
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
import xhtml2pdf.pisa
from customers.models import Customer
from orders.models import MailOrder, Order


@login_required
@render_to('orders/list.html')
def list(request):
    orders = request.user.customer.orders.all()
    return locals()


@user_passes_test(lambda u: u.is_superuser)
@login_required
@render_to('orders/fulfillment.html')
def fulfillment(request):

    if request.POST:
        order = Order.objects.get(id=request.POST.get('order_id'))
        if not order.fulfilled:
            order.fulfill(tracking_number=request.POST.get('tracking_number'))
        else:
            messages.warning(request, 'Order already fulfilled')

    orders = Order.objects.filter(to_be_fulfilled__lte=date.today())
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
