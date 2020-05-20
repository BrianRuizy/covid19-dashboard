
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

from . import getdata, plots, maps


def index(request): 
    report_dict = report()
    trends_dict = trends()
    growth_dict = growth_plot()
    daily_growth = daily_growth_plot()
    world_map_dict = world_map()
    cases_dict = global_cases()
    
    context = dict(report_dict, **trends_dict, **growth_dict, **daily_growth, **cases_dict, **world_map_dict)

    return render(request, template_name='index.html', context=context)
    

def report():
    df = getdata.daily_report(date_string=None)
    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f'{(df.Deaths / df.Confirmed)*100:.02f}%'
    return {
        'num_confirmed': df.Confirmed,
        'num_recovered': df.Recovered,
        'num_deaths': df.Deaths,
        'death_rate': death_rate }
    

def trends():
    df = getdata.percentage_trends()
    return {
        'confirmed_trend': df.Confirmed, 
        'deaths_trend': df.Deaths, 
        'recovered_trend': df.Recovered, 
        'death_rate_trend': df.Death_rate }
    

def growth_plot():
    plot_div = plots.total_growth()
    return {'growth_plot': plot_div}
    

def global_cases():
    df = getdata.global_cases()
    return {'global_cases': df}


def daily_growth_plot():
    plot_div = plots.daily_growth()
    return {'daily_growth_plot': plot_div}
    

def world_map():
    plot_div = maps.world_map()
    return {'world_map': plot_div}


def mapspage(request):
    plot_div = maps.usa_map()
    return render(request, template_name='pages/maps.html', context={'usa_map': plot_div})
