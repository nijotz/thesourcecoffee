from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from rewards.forms import EmailListForm

@login_required
@render_to('rewards/home.html')
def home(request):
    email_list_form = EmailListForm(request.POST or None)
    if request.method == 'POST':
        if email_list_form.is_valid():
            email_addresses = email_list_form.cleaned_data["list_of_emails"]
            email_success = True
    return locals()
