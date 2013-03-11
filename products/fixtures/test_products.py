from mezzanine.pages.models import Page
from products.models import Product

light = {
    'pk': 1,
    'title': "Lithuanian Light Roast",
    'content': "<p>Light roast coffee beans from Lithuania</p>"
}
dark = {
    'pk': 2,
    'title': "Damn Fine Dark Roast",
    'content': "<p>Dark roast coffee beans that are damn fine</p>"
}
medium = {
    'pk': 3,
    'title': "Miraculous Medium Roast",
    'content': "<p>Medium roast coffee beans that are, you know, pretty good</p>"
}

for product_data in (dark, medium, light):

    product_data['image'] = "products/coffee_beans.jpg"

    try:
        Product.objects.get(pk=product_data['pk']).delete()
    except Product.DoesNotExist:
        pass

    product = Product.objects.create(**product_data)
    product.page_ptr.parent = Page.objects.get(title='Products')
    product.page_ptr.save()
