from base.models import SiteSetting
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
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
    code = inviter.invite_code()
    invite_url = "https://{current_site}{signup_url}?code={code}".format(
        current_site=current_site,
        signup_url=signup_url,
        code=code)
    context = Context({
        "STATIC_URL": settings.STATIC_URL,
        "current_site": current_site,
        "invite_url": invite_url
    })

    invite_email_subject = SiteSetting.objects.get(key="rewards.invite_email_subject")

    rendered_html_template = loader.render_to_string("rewards/invite_email.html", context_instance=context)
    rendered_txt_template = loader.render_to_string("rewards/invite_email.txt", context_instance=context)
    email = EmailMultiAlternatives(invite_email_subject,
        rendered_txt_template,
        "The Source Coffee <noreply@thesourcecoffee.com>",
        [email_address])
    email.attach_alternative(rendered_html_template, "text/html")
    email.send(fail_silently=False)

