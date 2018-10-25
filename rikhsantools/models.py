# from __future__ import unicode_literals

from django.db import models
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils import timezone
from datetime import datetime, timedelta
# from rikhsantools import settings

# class Visitor(models.Model):
#     # title = models.CharField(max_length=255, blank=True)
#     id_visitor= models.AutoField(primary_key=True)
#     visited_at = models.DateTimeField(auto_now_add=True)

class Imagetopdf(models.Model):
    id_imagetopdf= models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='imagetopdf/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255, blank=True)

class Pdfscombine(models.Model):
    id_pdfscombine= models.AutoField(primary_key=True)
    pdf = models.FileField(upload_to='pdfcombine/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255, blank=True)

# class Pdf(models.Model):
#     # title = models.CharField(max_length=255, blank=True)
#     id_pdf= models.AutoField(primary_key=True)
#     filename= models.CharField(max_length=255, blank=True)
#     pdf = models.FileField(upload_to='pdf/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     visitor= models.ForeignKey(Visitor, on_delete=models.SET_NULL,null=True)
