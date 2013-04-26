from customers.tests import signup_test_customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


@user_passes_test(lambda u: u.is_superuser)
@login_required
def add_test_customer(request):
    signup_test_customer(request.POST)
    messages.info(request, 'Test customer added')
    return redirect(reverse('admin:index'))
