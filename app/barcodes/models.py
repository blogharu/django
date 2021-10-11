from django.db import models

# Create your models here.

class Barcode(models.Model):
    name = models.CharField(max_length=128)
    barcode = models.CharField(max_length=13)

