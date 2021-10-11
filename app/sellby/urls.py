from django.urls import path, include
from . import views

app_name = 'sellby'

urlpatterns = [
    path('', views.index, name='index'),    
    path('calendar/', views.calendar, name='calendar'),
    path('detail/', views.detail, name='detail'),
    path('add/record', views.add_record, name='add_record'),
]
