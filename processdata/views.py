from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from . import getdata

from plotly.offline import plot
from plotly.graph_objs import Layout
import plotly.graph_objs as go

def index(request): 
    report_dict = report()
    trends_dict = trends()
    growth_dict = growth_plot()
    context = dict(report_dict, **trends_dict, **growth_dict)
    
    return render(request, template_name='index.html', context=context)

def report():
    df = getdata.daily_report()
    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f"{(df.Deaths / df.Confirmed)*100:.03f}%"
    return {
        'num_confirmed': f'{df.Confirmed:,}',
        'num_recovered': f'{df.Recovered:,}',
        'num_deaths': f'{df.Deaths:,}',
        'death_rate': death_rate }
    

def trends():
    trends = getdata.percentage_trends()
    return {
        'confirmed_trend': trends.Confirmed, 
        'deaths_trend': trends.Deaths, 
        'recovered_trend': trends.Recovered, 
        'death_rate_trend': trends.death_rate }
    

def growth_plot():
    growth_df = getdata.realtime_growth()
    
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark', showlegend=False)
    fig = go.Figure(layout=layout)

    confirmed = go.Scatter(x=growth_df.index, y=growth_df.Confirmed, name='Confirmed', mode='lines+markers')
    deaths = go.Scatter(x=growth_df.index, y=growth_df.Deaths, name='Deaths', mode='lines+markers')
    recovered = go.Scatter(x=growth_df.index, y=growth_df.Recovered, name='Recovered', mode='lines+markers')

    traces = [confirmed, deaths, recovered]
    fig.add_traces(traces)
    plot_div = plot(fig, output_type='div')
    
    return {'plot_div': plot_div}
