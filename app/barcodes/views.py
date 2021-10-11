from django.shortcuts import render, redirect
from .forms import BarcodeForm
from .models import Barcode
from sellby.models import Record
from django.urls import reverse

# Create your views here.

def addBarcode(request):
    context = {}
    if 'barcode' in request.GET:
        context['barcode'] = request.GET['barcode']
    if 'expiryDate' in request.GET:
        context['expiryDate'] = request.GET['expiryDate']
    if request.POST:
        form = BarcodeForm(request.POST)
        if form.is_valid():
            curBarcode = Barcode(barcode=request.POST.get('barcode'), name=request.POST.get('name'))
            curBarcode.save()
            if 'barcode' in context and 'expiryDate' in context:
                Record(barcode=curBarcode,expiryDate=context['expiryDate'],user=request.user).save()
            return redirect(reverse('sellby:add_record')+"?isSuccess=True")
    return render(request, 'barcodes/add_barcode.html', context)