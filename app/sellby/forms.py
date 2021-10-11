from django import forms
from sellby.models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['barcode','expiryDate']

