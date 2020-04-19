from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from . import getdata

from plotly.offline import plot
from plotly.graph_objs import Layout
import plotly.graph_objs as go

def report(request):
    df = getdata.daily_report()
    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f"{(df.Deaths / df.Confirmed)*100:.03f}%"
    trends = getdata.percentage_trends()
    
    growth_df = getdata.realtime_growth()
    
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark', hovermode='x')
    fig = go.Figure(layout=layout)

    confirmed = go.Scatter(x=growth_df.index, y=growth_df.Confirmed, name='Confirmed', mode='lines+markers')
    deaths = go.Scatter(x=growth_df.index, y=growth_df.Deaths, name='Deaths', mode='lines+markers')
    recovered = go.Scatter(x=growth_df.index, y=growth_df.Recovered, name='Recovered', mode='lines+markers')


    traces = [confirmed, deaths, recovered]
    fig.add_traces(traces)
    
    plot_div = plot(fig, output_type='div')
        
    return render(request, 'index.html', {
        'num_confirmed': f'{df.Confirmed:,}',
        'num_recovered': f'{df.Recovered:,}',
        'num_deaths': f'{df.Deaths:,}',
        'death_rate': death_rate,
        'confirmed_trend': trends.Confirmed, 
        'deaths_trend': trends.Deaths, 
        'recovered_trend': trends.Recovered, 
        'death_rate_trend': trends.death_rate,
        'plot_div': plot_div,
        })

# def growth(request):
#     growth_df = getdata.realtime_growth()
#     fig = go.Figure()
#     traces = []
    
#     # for col in growth_df.columns:
#     #     col = go.Scatter(x=growth_df.index, y=growth_df[col], name=col, mode='lines+markers')
#     #     traces.append(col)
    
#     Confirmed = go.Scatter(x=growth_df.index, y=growth_df.Confirmed, name='Confirmed', mode='lines+markers')
    
#     fig.add_trace(Confirmed)
#     plot_div = plot(fig, output_type='div')
    
#     return render(request, 'index.html', context={'plot_div': plot_div})