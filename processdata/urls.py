from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('maps.html', views.mapspage, name='maps'),

]
