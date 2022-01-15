import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime



# Fetching Data from Yahoo Finance API
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 3)
df = web.DataReader(['AMZN','GOOGL','FB','AAPL','MSFT','ADBE','ALEX','NTES','ANF','APD','TSM','INTC','NVDA','NFLX','BAC','TWTR','WMT','PFE','MRNA','BNTX'],
                    'yahoo', start=start, end=end)

df = df.stack().reset_index()


# Initailizing the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )




# App Layout
app.layout=dbc.Container([
     dbc.Row([
          dbc.Col(html.H2('Stock Market DataViewer',
                         className='text-center text-dark mt-5 mb-5'),width=12)
     ]),

     dbc.Row([
          dbc.Col([
               dcc.Dropdown(id='dpdn-1',multi=False,value='AMZN',
                         options=[{'label':x,'value':x}
                                   for x in sorted(df['Symbols'].unique())],
                                   style={
                                   
                                   "background": '#111111',
                              },
               ),
               dbc.Card([dbc.CardBody(
                dcc.Graph(id='fig-1',figure={})
               )])
          ]),

          dbc.Col([
               dcc.Dropdown(id='dpdn-2', multi=True, value=['PFE','BNTX'],
                              options=[{'label':x, 'value':x}
                                   for x in sorted(df['Symbols'].unique())],
                              style={
                                   
                                   "background": '#111111',
                              },),
               dbc.Card([dbc.CardBody(
                dcc.Graph(id='fig-2', figure={})
               )])
          ]),

     ]),

     dbc.Row([

          dbc.Col([
               html.P("Select Company Stock:",
                    className='text-dark mt-5'),
               dcc.Checklist(id='checklist', value=['FB', 'GOOGL', 'AMZN', 'AAPL', 'NFLX', 'NVDA', 'TWTR'],
                              options=[{'label':x, 'value':x}
                                        for x in sorted(df['Symbols'].unique())],
                              labelClassName="mr-3"
                              ),
               dbc.Card([dbc.CardBody(
                dcc.Graph(id='fig-3', figure={})
               )])
               
          ],className='mb-5')
     ]),
])


# Adding Callbacks
# Line chart - Single
@app.callback(
    Output('fig-1', 'figure'),
    Input('dpdn-1', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols']==stock_slctd]
    figln = px.line(dff, x='Date', y='High',template='plotly_dark')
    return figln


# Line chart - multiple
@app.callback(
    Output('fig-2', 'figure'),
    Input('dpdn-2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols',template='plotly_dark')
    return figln2


# Histogram
@app.callback(
    Output('fig-3', 'figure'),
    Input('checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date']=='2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close',template='plotly_dark')
    return fighist



if __name__=='__main__':
     app.run_server(debug=True)
