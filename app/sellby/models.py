from django.db import models
from django.contrib.auth.models import User
from barcodes.models import Barcode

# Create your models here.

class Record(models.Model):
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiryDate = models.DateField()
    isRemoved = models.BooleanField(default=True)
