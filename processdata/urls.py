from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('maps.html', views.mapspage, name='maps'),
    path('report', views.report, name='report'),
    path('trends', views.trends, name='trends'),
    path('cases', views.global_cases, name='cases'),
    path('realtime_growth', views.realtime_growth, name='realtime_growth'),
    path('daily_growth', views.daily_growth, name='daily_growth'),
    path('daily_report', views.daily_report, name='daily_report')
]
