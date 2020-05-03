
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
    # spark_dict = sparklines()
    
    context = dict(report_dict, **trends_dict, **growth_dict, **daily_growth, **cases_dict,)

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
    df = getdata.realtime_growth()
    dates = pd.to_datetime(df.index)
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)',  plot_bgcolor='rgba(0,0,0,0)', yaxis_type='log', xaxis_showgrid=False, template='plotly_dark',  legend=dict(x=0.025, y=1),  font=dict(color='#8898aa'),  height=310, margin=dict(t=0, l=15, r=10, b=0))
    fig = go.Figure(layout=layout)
    
    confirmed = go.Scatter(x=dates, y=df.Confirmed, name='Confirmed', mode='lines', line=dict(width=4), marker_color='#6236ff')
    recovered = go.Scatter(x=dates, y=df.Recovered, name='Recovered', mode='lines', line=dict(width=4), marker_color='#2dce89')
    deaths = go.Scatter(x=dates, y=df.Deaths, name='Deaths', mode='lines', line=dict(width=4), marker_color='#f9345e')

    fig.add_traces([confirmed, deaths, recovered])
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})

    return {'growth_plot': plot_div}
    
    
def daily_growth_plot():
    dcases = getdata.daily_cases()[['date', 'World']]
    ddeaths = getdata.daily_deaths()[['date', 'World']]
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)',  plot_bgcolor='rgba(0,0,0,0)', legend=dict(x=0.025, y=1), height=310, margin=dict(t=0, l=15, r=10, b=0), barmode='stack')
    fig = go.Figure(layout=layout)
    
    ddeaths_trace = go.Bar(x=ddeaths.date, y=ddeaths.World, name='Deaths', marker_color='#f9345e')
    dcases_trace = go.Bar(x=dcases.date, y=dcases.World, name='Cases', marker_color='#6236ff', visible='legendonly')
    
    fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=7, label='W', step='day', stepmode='backward'),
            dict(count=1, label='M', step='month', stepmode='backward'),
            dict(count=3, label='3M', step='month', stepmode='backward'),
            dict(label='T', step='all')
        ]))
    )
    fig.update_yaxes(gridcolor='#e9ecef')
    fig.add_traces([dcases_trace, ddeaths_trace])
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})
    
    return {'daily_growth_plot': plot_div}


# def sparklines():
#     df = getdata.realtime_growth()
#     layout = Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_type='log', xaxis_showgrid=False, height=250, width=280, xaxis=dict(showgrid= False,zeroline= False,visible=False, fixedrange=True), yaxis=dict(showgrid= False,zeroline= False,visible=False, fixedrange=True))

#     recovered = go.Scatter(x=df.index, y=df.Recovered,  mode='lines', line=dict(width=4), marker_color='#2dce89')
#     deaths = go.Scatter(x=df.index, y=df.Deaths,  mode='lines', line=dict(width=4), marker_color='#f9345e')
    
#     confirmed = go.Figure(layout=layout).add_trace(go.Scatter(x=df.index, y=df.Confirmed, mode='lines', line=dict(width=4), marker_color='#6236ff', fill='toself', fillcolor='rgba(98,54,255,0.08)'))
    
#     plot_div1 = plot(confirmed, output_type='div', config={'displayModeBar': False})

#     return {'sparkline': plot_div1}

def cases_table():
    df = getdata.cases_table()
    return {'cases_table': df}