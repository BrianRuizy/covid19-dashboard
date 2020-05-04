from plotly.offline import plot
from plotly.graph_objs import Layout
import plotly.graph_objs as go

import pandas as pd
from . import getdata


def total_growth():
    df = getdata.realtime_growth()
    dates = pd.to_datetime(df.index)
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)',  plot_bgcolor='rgba(0,0,0,0)', yaxis_type='log', xaxis_showgrid=False, template='plotly_dark',  legend=dict(x=0.025, y=1),  font=dict(color='#8898aa'),  height=310, margin=dict(t=0, l=15, r=10, b=0))
    fig = go.Figure(layout=layout)
    
    confirmed = go.Scatter(x=dates, y=df.Confirmed, name='Confirmed', mode='lines', line=dict(width=4))
    recovered = go.Scatter(x=dates, y=df.Recovered, name='Recovered', mode='lines', line=dict(width=4))
    deaths = go.Scatter(x=dates, y=df.Deaths, name='Deaths', mode='lines', line=dict(width=4), marker_color='#f5365c')

    fig.add_traces([confirmed, deaths, recovered])
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})

    return plot_div
    
    
def daily_growth():
    dcases = getdata.daily_cases()[['date', 'World']]
    ddeaths = getdata.daily_deaths()[['date', 'World']]
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)',  plot_bgcolor='rgba(0,0,0,0)', legend=dict(x=0.025, y=1), height=310, margin=dict(t=0, l=15, r=10, b=0), barmode='stack')
    fig = go.Figure(layout=layout)
    
    ddeaths_trace = go.Bar(x=ddeaths.date, y=ddeaths.World, name='Deaths', marker_color='#f5365c')
    dcases_trace = go.Bar(x=dcases.date, y=dcases.World, name='Cases', visible='legendonly')
    
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
    
    return plot_div
    