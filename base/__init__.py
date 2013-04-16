from django.contrib import admin as django_admin
from mezzanine.boot.lazy_admin import LazyAdminSite
from base.admin import get_admin_site

admin_site = get_admin_site(LazyAdminSite)
django_admin.site = admin_site
