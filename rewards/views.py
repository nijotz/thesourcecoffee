from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required

@login_required
@render_to('rewards/home.html')
def home(request):
    return locals()
