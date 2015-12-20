from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models

@python_2_unicode_compatible
class Composition(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.title
