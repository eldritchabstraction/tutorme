# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=30)
    last_name = models.TextField(max_length=30)
    birth_date = models.DateField()
    star_power = models.IntegerField(default=5)
    email = models.EmailField(max_length=254)
    email_confirmed = models.BooleanField(default=0)

    def __unicode__(self):
        return self.first_name + " " + self.last_name
