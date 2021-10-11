from django import forms
from barcodes.models import Barcode


class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode
        fields = ['barcode','name']

