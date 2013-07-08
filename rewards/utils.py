from base.models import SiteSetting
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template import Context, loader
HASH_LETTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62encode(num_to_encode):
    code = []
    while (num_to_encode > 0):
        # base62 encoding stuff
        remainder = num_to_encode % 62
        num_to_encode = num_to_encode // 62
        code.append(remainder)

    return reduce(lambda accum, num: accum + HASH_LETTERS[num], code, "")

def send_invite_email(inviter, email_address):
    signup_url = reverse("signup")
    current_site = Site.objects.get(name="Default").domain
    invite_url = "https://{current_site}{signup_url}?code={code}".format(
        current_site=current_site,
        signup_url=signup_url,
        code="BLABLABLA")
    context = Context({
        "STATIC_URL": settings.STATIC_URL,
        "current_site": current_site,
        "invite_url": invite_url
    })
    invite_email_subject = SiteSetting.objects.get(key="rewards.invite_email_subject")

