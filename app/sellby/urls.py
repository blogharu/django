from django.urls import path, include
from . import views

app_name = 'sellby'

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar, name='calendar'),
    path('details/', views.details, name='details'),
    path('add/record', views.add_record, name='add_record'),
]
