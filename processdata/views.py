from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from . import getdata


def report(request):
    df = getdata.daily_report()
    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f"{(df.Deaths / df.Confirmed)*100:.03f} %"
    
    trends = getdata.percentage_trends()
    
    growth = getdata.realtime_growth(weekly=True)
    
    return render(request, 'index.html', {
        'num_confirmed': f'{df.Confirmed:,}',
        'num_recovered': f'{df.Recovered:,}',
        'num_deaths': f'{df.Deaths:,}',
        'death_rate': death_rate,
        'confirmed_trend': trends.Confirmed, 
        'deaths_trend': trends.Deaths, 
        'recovered_trend': trends.Recovered, 
        'death_rate_trend': trends.death_rate,
        'weekly_confirmed': growth.Confirmed.values,
        })
