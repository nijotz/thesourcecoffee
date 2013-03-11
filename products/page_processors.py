from mezzanine.pages.page_processors import processor_for
from subscriptions.models import CustomerSubscription, Subscription
from products.models import Product

@processor_for(Product)
def customer_subscriptions_for_product(request, page):

    context = {
        'subscription_types': None, 
        'subscriptions': None
    }

    if not request.user.is_authenticated():
        return context

    product = page.product
    context['subscription_types'] = Subscription.objects.filter(product=product).order_by('subscription_type__amount')
    context['subscriptions'] = CustomerSubscription.objects.filter(
        customer=request.user,
        subscription__product=product
    )

    return context
