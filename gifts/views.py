from django.http import HttpResponse
import json
from gifts.models import GiftSubscription

def check_code(request):
    code = request.REQUEST.get('code', '')
    email = request.REQUEST.get('email', '')
    try:
        gift = GiftSubscription.objects.get(
            code__code=code,
            giftee=email)
        return HttpResponse('true')
    except:
        return HttpResponse('false')
