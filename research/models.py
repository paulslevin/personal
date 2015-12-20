from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import re

@python_2_unicode_compatible
class Coauthor(models.Model):
    coauthor = models.CharField(max_length=500)
    institution = models.CharField(max_length=500)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.coauthor

@python_2_unicode_compatible
class Paper(models.Model):
    doi = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=500)
    coauthors = models.ManyToManyField(Coauthor, blank=True, null=True)
    publish_date = models.DateField('date published', blank=True, null=True)
    address = models.URLField(max_length=200)

    def __str__(self):
        return self.title

    def get_short_title(self):
        short = self.title.lower().split()[0]
        return re.sub(r'\W+', '', short)
        
