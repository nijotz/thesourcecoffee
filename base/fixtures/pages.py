from mezzanine.pages.models import Page, RichTextPage

pages = [
    {
        'title': 'About Us',
        'content': "We're Awesome",
    },
    {
        'title': 'Products',
        'content': 'Awesome products',
    },
    {
        'title': 'Contact Us',
        'content': '555-555-5555',
    }
]

order = 0
for page_data in pages:

    try:
        RichTextPage.objects.get(title=page_data['title']).delete()
    except RichTextPage.DoesNotExist:
        pass

    RichTextPage.objects.create(_order=order, **page_data)

    order += 1
