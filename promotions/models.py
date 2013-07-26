import random

from django.db import models, IntegrityError
from promotions.settings import PROMO_CODE_CHARS as chars
from promotions.settings import PROMO_CODE_LENGTH as length

def random_code():
    return ''.join(random.choice(chars) for x in xrange(length))

class Code(models.Model):
    code = models.CharField(max_length=length, primary_key=True)

    def save(self, *args, **kwargs):
        if self.code:
            return super(PromoCode, self).save(*args, **kwargs)
        else:
            for x in xrange(10):
                self.pk = random_code()
                try:
                    return super(Code, self).save(*args, **kwargs)
                except IntegrityError:
                    pass
        raise Exception('Could not generate unique invite code')
