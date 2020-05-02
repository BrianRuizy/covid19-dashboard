
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from . import getdata

from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Layout
import pandas as pd


def index(request): 
    report_dict = report()
    trends_dict = trends()
    growth_dict = growth_plot()
    daily_growth = daily_growth_plot()
    cases_dict = cases_table()
    
    context = dict(report_dict, **trends_dict, **growth_dict, **daily_growth, **cases_dict)
    
    return render(request, template_name='index.html', context=context)


def report():
    df = getdata.daily_report(date_string=None)
    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f"{(df.Deaths / df.Confirmed)*100:.02f}%"
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
    df = getdata.realtime_growth()
    domain = pd.to_datetime(df.index)
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)',  plot_bgcolor='rgba(0,0,0,0)', xaxis_showgrid=False, template='plotly_dark',  legend=dict(x=0.025, y=1),  font=dict(color='#8898aa'),  height=350, margin=dict(t=0, l=15, r=10, b=0))
    fig = go.Figure(layout=layout)
    
    confirmed = go.Scatter(x=domain, y=df.Confirmed, name='Confirmed', mode='lines', line=dict(width=4))
    recovered = go.Scatter(x=domain, y=df.Recovered, name='Recovered', mode='lines', line=dict(width=4))
    deaths = go.Scatter(x=domain, y=df.Deaths, name='Deaths', mode='lines', line=dict(width=4), marker_color='#f5365c')

    fig.add_traces([confirmed, deaths, recovered])
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})

    return {'growth_plot': plot_div}
    
    
def daily_growth_plot():
    dcases = getdata.daily_cases()[['date', 'World']]
    ddeaths = getdata.daily_deaths()[['date', 'World']]
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)',  plot_bgcolor='rgba(0,0,0,0)', legend=dict(x=0.025, y=1), height=350, margin=dict(t=0, l=15, r=10, b=0))
    fig = go.Figure(layout=layout)
    
    ddeaths_trace = go.Bar(x=ddeaths.date, y=ddeaths.World, name='Deaths', marker_color='#f5365c')
    dcases_trace = go.Bar(x=dcases.date, y=dcases.World, name='Cases', visible='legendonly')
    
    fig.update_layout(barmode='stack', )
    fig.update_yaxes(gridcolor='#e9ecef')
    fig.add_traces([dcases_trace, ddeaths_trace])

    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})
    
    return {'daily_growth_plot': plot_div}
    

def cases_table():
    df = getdata.cases_table()
    return {'cases_table': df}