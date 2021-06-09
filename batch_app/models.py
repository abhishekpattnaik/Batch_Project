import string, random
from django.db import models
from django.contrib.auth.models import User
from constants.constant import ALPHANUMERICLEN

class Batch(models.Model):
    name = models.CharField(max_length=254, blank=True, default="")
    batch_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.name

class Code(models.Model):
    batch = models.ForeignKey("batch_app.Batch", on_delete=models.CASCADE, null=True, blank=True)
    batch_code = models.CharField(max_length=ALPHANUMERICLEN, blank=False)

    def save(self, *args, **kwargs):
        letters = string.ascii_lowercase
        self.batch_code = ''.join(random.choice(letters) for i in range(ALPHANUMERICLEN))
        super(Code, self).save(*args, **kwargs)

    def __str__(self):
        return self.batch_code
