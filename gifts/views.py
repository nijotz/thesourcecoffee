from annoying.decorators import render_to
from django.http import HttpResponse
import json
from gifts.models import GiftSubscription

def check_code(request):
    code = request.REQUEST.get('code', '')
    try:
        gift = GiftSubscription.objects.get(code__code=code)
        data = {}
        data['interval'] = gift.plan.interval
        data['amount'] = gift.plan.amount
        return HttpResponse(json.dumps(data))
    except:
        return HttpResponse(json.dumps(None))

@render_to('gifts/purchased.html')
def purchased(request):
    gift = None
    gift_id = request.session.get('gifts_purchased', None)
    if gift_id:
        try:
            gift = GiftSubscription.objects.get(id=gift_id)
        except:
            pass
    return {'gift':gift}
