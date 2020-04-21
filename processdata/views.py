from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from . import getdata

from plotly.offline import plot
from plotly.graph_objs import Layout
import plotly.graph_objs as go
from datetime import datetime

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
    
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark', showlegend=False, font=dict(color='#8898aa'),  margin=dict(t=0, l=0, r=0))
    fig = go.Figure(layout=layout)
    domain = []
    
    for date in range(len(growth_df.index)):
        domain.append(datetime.strptime(growth_df.index[date], '%m/%d/%y').strftime('%-m/%-d'))
    
    confirmed = go.Scatter(x=domain, y=growth_df.Confirmed, name='Confirmed', mode='lines', line=dict(width=4))
    deaths = go.Scatter(x=domain, y=growth_df.Deaths, name='Deaths', mode='lines', line=dict(width=4))
    recovered = go.Scatter(x=domain, y=growth_df.Recovered, name='Recovered', mode='lines', line=dict(width=4))

    traces = [confirmed, deaths, recovered]
    fig.add_traces(traces)
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})
    
    
    return {'plot_div': plot_div}
