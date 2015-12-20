from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Polynomial(models.Model):
    polynomial = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.polynomial
