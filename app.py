import dash
#from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import flask
from flask_cors import CORS
import os


'''
By Vivien Lee
iota Chapter Potential Alpha Delta Class
'''

df = pd.read_csv('data.csv',sep='|')
df.head()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                        "//fonts.googleapis.com/css?family=Dosis:Medium",
                        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]

app = dash.Dash(external_stylesheets=external_stylesheets)

for css in external_stylesheets:
    app.css.append_css({"external_url": css})

server = app.server

df['text'] = '<b>' + df['project'].astype(str) + '</b><br><br>' # + df['desc'].astype(str)


data = [ dict(
        type = 'scattergeo',
        locationmode = 'ISO-3',
        lon = df['long'],
        lat = df['lat'],
        hoverinfo = 'text',
        text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 20,
            opacity = 1,
            reversescale = True,
            symbol = 'diamond-wide-dot',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            color = 'rgb(0, 200, 0)',

        ))]

layout = dict(
        title = 'CUSD - Sustainable Education',
        width = 1400,
        height = 700,
        geo = dict(
            scope='world',
            projection=dict( type='equirectangular' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5,
            showcountries = True,
        ),
    )

fig = dict( data=data, layout=layout)

app.layout  = html.Div(children=[


                dcc.Graph(id='graph', figure=fig),



], style={'backgroundColor':'white'})


#server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
