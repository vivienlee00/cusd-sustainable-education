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

df['text'] = '<b>' + df['project'].astype(str) + '</b>' # + df['desc'].astype(str)


data = [ dict(
        type = 'scattergeo',
        locationmode = 'ISO-3',
        lon = df['long'],
        lat = df['lat'],
        hoverinfo = 'text',
        customdata = df['project'],
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
        width = 700,
        height = 450,
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
STARTING_PROJECT = 'Sustainable Education Nepal'
STARTING_DESC = df.loc[df['project'] == STARTING_PROJECT]['desc'].iloc[0]
STARTING_IMG = "https://cusd.cornell.edu/images/project-photos/snn-2-ff43fd96.jpg"


app.layout  = html.Div(children=[

                dcc.Graph(id='graph', figure=fig, style=dict(float='left')),

                html.Div(children= [
                    html.H5(STARTING_PROJECT,
                    id='project_name', style=dict(marginBottom='10px',textAlign='left',fontSize='25px')),

                    html.P(STARTING_DESC,
                    id='description',
                    style=dict(fontSize='16px', marginBottom='15px', fontWeight='lighter')),

                    html.Img(id='proj_img', src=STARTING_IMG, style={'width':'320px', 'height':'auto', 'position': 'absolute', 'clip':'rect(0px,500px,350px,0px)'}),

                ], style={'float':'right','width':'320px','margin-right':'390px'})

], style={'backgroundColor':'white','display':'inline'})


def dfRowFromHover( hoverData ):
    ''' Returns row for hover point as a Pandas Series '''
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                project_name = str(fig['data'][0]['text'][point_number]).strip()
                return df.loc[df['project'] == project_name]
    return pd.Series()

@app.callback(
    dash.dependencies.Output('project_name', 'children'),
    [dash.dependencies.Input('graph', 'hoverData')])
def return_chapter_name(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'customdata' in firstPoint:
                project = firstPoint['customdata']
                return project
    return STARTING_PROJECT

@app.callback(
    dash.dependencies.Output('description', 'children'),
    [dash.dependencies.Input('graph', 'hoverData')])
def return_chapter_name(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'customdata' in firstPoint:
                project = firstPoint['customdata']
                return df.loc[df['project'] == project]['desc'].iloc[0]
    return STARTING_DESC

@app.callback(
    dash.dependencies.Output('proj_img', 'src'),
    [dash.dependencies.Input('graph', 'hoverData')])
def return_chapter_name(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'customdata' in firstPoint:
                project = firstPoint['customdata']
                return df.loc[df['project'] == project]['img'].iloc[0]
    return STARTING_IMG


#server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
