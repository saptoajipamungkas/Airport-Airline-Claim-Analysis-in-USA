#  Ujian Modul 2
# Nama    : Sapto Aji Pamungkas
# Kelas   : JC DS Purwadhika Batch 7

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import seaborn as sns
import dash_table
from dash.dependencies import Input, Output, State

def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
    )

df = pd.read_csv('tsa_claims_ujian.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1('Ujian Modul 2 Dashboard TSA'),
        html.Div(children='''
        Created by: Sapto Aji Pamungkas
    '''),
        dcc.Tabs(children=[
                dcc.Tab(value='Tab1', label='DataFrame Table',children=[ 
                html.Div([
                        html.P('Claim Site'),
                        dcc.Dropdown(value='',
                        id='filter-claimsite',
                        options=[{'label':i,'value':i} for i in df['Claim Site'].unique()])
                    ],className='col-3'),

                    html.Div(id='dataTable',
                        children=[generate_table(df)],className = 'col-3')]),
                    
    
                dcc.Tab(value='Tab2', label='Bar-Chart',className='col-3'),

                dcc.Tab(value='Tab3', label='Scatter-Chart', children=[
                    html.Div(children=dcc.Graph(
                                id='graph-scatter',
                                figure = {'data':[
                                    go.Scatter(
                                        x=df[df['Claim Type']==i]['Claim Amount'],
                                        y=df[df['Claim Type']==i]['Close Amount'],
                                        mode='markers',
                                        name='Claim type{}'.format(i)
                                        )for i in  df['Claim Type'].unique()
                                    ],
                                    'layout':go.Layout(
                                        xaxis={'title':'Claim Amount'},
                                        yaxis={'title':'Close Amount'},
                                        title=' Scatter - Chart',
                                        hovermode='closest'
                            )
                        }
                        ))], 
                        className='col-3'),

                dcc.Tab(value='Tab4', label='Pie-Chart', children=[

                    html.Div(children=[
                            (html.P('Claim Site'),
                                dcc.Dropdown(value='',
                                id='filter-claimsite',
                                options=[{'label':i,'value':i} for i in df['Claim Site'].unique()]))]
                            ,className='col-3')

                    ,dcc.Graph(
                                id='graph-pie',
                                figure = {
                                    'data':[
                                        go.Pie(
                                        labels=df['Claim Type'].unique(),
                                        values=[(df[df['Claim Type']=='Property Damage']['Claim Type'].mean()), 
                                                (df[df['Claim Type']=='Passenger Property Loss']['Claim Type'].mean()),
                                                (df[df['Claim Type']=='Employee Loss (MPCEA)']['Claim Type'].mean()),
                                                (df[df['Claim Type']=='Passenger Theft']['Claim Type'].mean())]
                                        )],
                                'layout': {
                                    'title': 'Claim Type'
                                    }
                                }
                            )                
                    ],className='col-3'),
            ], className='row')
            ])

if __name__ == '__main__':
    app.run_server(debug=True)
