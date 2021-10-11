from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecordForm
from . import helpers
import barcodes.helpers
from .models import Record
from barcodes.models import Barcode
from django.urls import reverse

# Create your views here.

@login_required(login_url='/users/login/')
def calendar(request):
    context = helpers.initCalendarContext(int(request.GET.get('year', 0)), int(request.GET.get('month', 0)))
    return render(request, 'sellby/calendar.html', context)

@login_required(login_url='/users/login/')
def index(request):
    context = helpers.initIndexContext(10)
    return render(request, 'sellby/index.html', context)

@login_required(login_url='/users/login/')
def detail(request):
    context = {}
    return render(request, 'sellby/detail.html', context)


@login_required(login_url='/users/login/')
def add_record(request):
    context = {}
    if 'isSuccess' in request.GET:
        context["isSuccess"] = True
    if request.method == "POST":
        result = {}
        result["expiryDate"] = request.POST["expiry-date"]
        if result["expiryDate"] and 'expiry-date-image' in request.FILES:
            helpers.saveExpiryImage(request)
        if 'barcode' in request.FILES:
            barcode = barcodes.helpers.djangoImg2Barcode(request)
            print(barcode)
            if barcode:
                barcode = barcode.decode('utf-8')
                barcodesFilter = Barcode.objects.filter(barcode=barcode)
                if len(barcodesFilter) == 0:
                    return redirect(reverse('barcodes:add_barcode')+'?barcode={}&expiryDate={}'.format(barcode, request.POST.get('expiry-date')))
                result["barcode"] = list(barcodesFilter.values())[-1]['id']
        form = RecordForm(result)
        if form.is_valid():
            Record(barcode=barcodesFilter.get(id=result["barcode"]), expiryDate=result["expiryDate"], user=request.user).save()
            context["isSuccess"] = True
            return render(request, 'sellby/record_form.html', context)
        context["form"] = form
    return render(request, 'sellby/record_form.html', context)



