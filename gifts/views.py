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
        data = {}
        data['interval'] = gift.plan.interval
        data['amount'] = gift.plan.amount
        return HttpResponse(json.dumps(data))
    except:
        return HttpResponse(json.dumps(None))
