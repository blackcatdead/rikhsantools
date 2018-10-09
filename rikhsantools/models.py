from __future__ import unicode_literals

from django.db import models
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils import timezone
from datetime import datetime, timedelta
# from rikhsantools import settings

class Visitor(models.Model):
    # title = models.CharField(max_length=255, blank=True)
    id_visitor= models.AutoField(primary_key=True)
    visited_at = models.DateTimeField(auto_now_add=True)

# class Photo(models.Model):
#     # title = models.CharField(max_length=255, blank=True)
#     id_photo= models.AutoField(primary_key=True)
#     photo = models.ImageField(upload_to='photos/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     visitor= models.ForeignKey(Visitor, on_delete=models.SET_NULL,null=True)

class Pdf(models.Model):
    # title = models.CharField(max_length=255, blank=True)
    id_pdf= models.AutoField(primary_key=True)
    filename= models.CharField(max_length=255, blank=True)
    pdf = models.FileField(upload_to='pdf/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    visitor= models.ForeignKey(Visitor, on_delete=models.SET_NULL,null=True)
