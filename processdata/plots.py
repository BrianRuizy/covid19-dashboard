# Standard library imports
import json 
from urllib.request import urlopen

# Third party imports
import pandas as pd 
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objs import Layout
from plotly.offline import plot

# Local application imports
from . import getdata

# file for creation of plotly figures(figs)
# you can use the plotly builtin fig.show() method to plot locally


def total_growth():
    """[summary] Plots cumulative growth in a logarithmic y-scale
    Reference: https://plotly.com/python/line-and-scatter/
    
    Returns:
        [plotly.graph_objs] -- [plot_div compatible with Django]
    """
    df = getdata.realtime_growth()
    dates = pd.to_datetime(df.index)
    layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_type='log',
        xaxis_showgrid=False,
        template='plotly_dark',
        showlegend=False,
        font=dict(color='#8898aa'),
        height=310,
        margin=dict(t=0, l=10, r=10, b=0)
    )
    fig = go.Figure(layout=layout)

    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                # direction="left",
                buttons=list([
                    dict(
                        args=[{"yaxis.type": "log"}],
                        label="Logarithmic",
                        method="relayout"
                    ),
                    dict(
                        args=[{"yaxis.type": "linear"}],
                        label="Linear",
                        method="relayout"
                    )
                ]),
                x=0.05,
                xanchor='auto',
                bgcolor='rgba(0,0,0,0)'
            ),
        ]
    )
    
    confirmed_trace = go.Scatter(x=dates, y=df.Confirmed, name='Confirmed', mode='lines', line=dict(width=4))
    recovered_trace = go.Scatter(x=dates, y=df.Recovered, name='Recovered', mode='lines', line=dict(width=4))
    deaths_trace = go.Scatter(x=dates, y=df.Deaths, name='Deaths', mode='lines', line=dict(width=4), marker_color='#f5365c')

    fig.add_traces([confirmed_trace, deaths_trace, recovered_trace])
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})

    return plot_div
    

def daily_growth():
    """[summary] Plots daily data of confirmations and deaths, as stacked bar
    Reference: https://plotly.com/python/bar-charts/
    
    Returns:
        [plotly.graph_objs] -- [plot_div compatible with Django]
    """
    daily_cases = getdata.daily_confirmed()[['date', 'World']]
    daily_deaths = getdata.daily_deaths()[['date', 'World']]
    layout = Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(x=0.025, y=1), height=310, margin=dict(t=0, l=15, r=10, b=0), barmode='stack')
    fig = go.Figure(layout=layout)
    daily_deaths_trace = go.Bar(x=daily_deaths.date, y=daily_deaths.World, name='Deaths', marker_color='#f5365c')
    daily_cases_trace = go.Bar(x=daily_cases.date, y=daily_cases.World, name='Cases', visible='legendonly')
    
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label='W', step='day', stepmode='backward'),
                dict(count=1, label='M', step='month', stepmode='backward'),
                dict(count=3, label='3M', step='month', stepmode='backward', ),
                dict(label='T', step='all')
            ]))
        )
    
    fig.update_yaxes(gridcolor='#fff')
    fig.add_traces([daily_cases_trace, daily_deaths_trace])
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})
    
    return plot_div
    

def worldmap():
    # Use following Mapbox token to acces further styling features.
    # Reference: https://plotly.com/python/reference/#scattermapbox
    
    # px.set_mapbox_access_token(open(".mapbox_token").read(''))

    df = getdata.daily_report()
    fig = px.scatter_mapbox(df, 
            lat="Lat", lon="Long_", color='Confirmed', hover_name="Country_Region", hover_data=["Combined_Key","Confirmed"],
            size='Confirmed', zoom=1, labels={'Combined_Key':'loc'}, center = {"lat": 20.0, "lon": -20.0}, height=450,)

    fig.update_layout(mapbox_style='carto-positron', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, l=0, r=0, b=0))
    plot_div = plot(fig, output_type='div', config={'displayModeBar': False})
    
    return plot_div

