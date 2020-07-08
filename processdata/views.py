
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

import json

from . import getdata, plots, maps


def index(request): 
    growth_dict = growth_plot()
    daily_growth = daily_growth_plot()
    world_map_dict = world_map()
    cases_dict = global_cases()

    context = dict(**growth_dict, **daily_growth, **cases_dict, **world_map_dict)

    return render(request, template_name='index.html', context=context)


def report(request):
    df = getdata.daily_report(date_string=None)
    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f'{(df.Deaths / df.Confirmed)*100:.02f}%'

    data = {
        'num_confirmed': int(df.Confirmed),
        'num_recovered': int(df.Recovered),
        'num_deaths': int(df.Deaths),
        'death_rate': death_rate
    }

    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')


def trends(request):
    df = getdata.percentage_trends()

    data = {
        'confirmed_trend': int(df.Confirmed),
        'deaths_trend': int(df.Deaths),
        'recovered_trend': int(df.Recovered),
        'death_rate_trend': float(df.Death_rate)
    }

    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')


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
