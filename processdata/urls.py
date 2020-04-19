from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.report, name='report'),
    # path('', views.growth, name='growth'),
]
