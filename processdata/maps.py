# File for creation of plotly maps(figs).
# You can use the plotly builtin fig.show() method to map locally.
import json
from urllib.request import urlopen

import plotly.graph_objs as go
from plotly.offline import plot

from . import getdata


def usa_map():
    # Map of USA subdivided by FIPS-codes (counties), showing cases per-capita basis
    # Reference: https://plotly.com/python/reference/#choroplethmapbox
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = getdata.usa_counties()
    df.drop([2311], inplace=True)

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson = counties, 
            locations = df.fips,
            z = df['cases/capita'],
            marker_opacity = 0.75,
            marker_line_width = 0,
            colorscale = [[0, '#FFFAF4'], [.005, '#FFE4CC'], [.030, '#DC654F'], [.060, '#CA3328'], [.080, '#B80000'], [.100, '#7C100C'], [.150, '#580000'], [.175, '#300000'], [1, '#170707']]
        )
    )

    fig.update_layout(
        mapbox_style = 'carto-positron', 
        paper_bgcolor='rgba(0,0,0,0)', 
        mapbox_zoom=2.75, 
        mapbox_center = {'lat': 37.0902, 'lon': -95.7129}, 
        margin = dict(t=0, l=0, r=0, b=0)
    )
    plot_div = plot(fig, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})

    return plot_div
