from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import Context
from rewards.forms import EmailListForm
from rewards.utils import send_invite_email

@login_required
@render_to('rewards/home.html')
def home(request):
    email_list_form = EmailListForm(request.POST or None)
    if request.method == 'POST':
        if email_list_form.is_valid():
            email_addresses = email_list_form.cleaned_data["list_of_emails"]
            for email in email_addresses:
                send_invite_email(request.user.customer, email)

            email_success = True
    return locals()

@login_required
def invite_email(request):
    if settings.DEBUG:
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
        return render_to_response("rewards/invite_email.html", context_instance=context)
    return HttpRedirect("rewards_home")
