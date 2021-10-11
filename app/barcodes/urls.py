from django.urls import path, include
from . import views

app_name = 'barcodes'

urlpatterns = [
    path('add/barcode', views.addBarcode, name="add_barcode")
]
