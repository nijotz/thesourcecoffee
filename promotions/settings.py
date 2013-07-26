import string
from django.conf import settings

PROMO_CODE_LENGTH = getattr(settings, 'PROMO_CODE_LENGTH', 6)
PROMO_CODE_CHARS = getattr(settings, 'PROMO_CODE_CHARS', string.letters + string.digits)
