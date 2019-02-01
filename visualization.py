import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime
import pandas as pd

# Initialize the app
app = dash.Dash()
server = app.server

# Create list of company tickers for drop down input
nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol',inplace=True)
options = []
for tic in nsdq.index:
  my_dict = {}
  my_dict['label'] = nsdq.loc[tic]['Name'] + ' ' + tic
  my_dict['value'] = tic
  options.append(my_dict)

# Define the layout of the app
app.layout = html.Div([
  html.H1('Interactive Stock Price Movement Chart'),
  html.Div([html.H3('Enter stock symbols:', style={'paddingRight':'30px'}),
            dcc.Dropdown(id = 'my_stock_picker', 
                         options = options, 
                         value = ['TSLA'], 
                         multi = True)
            ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
  html.Div([html.H3('Select a start and end date:'),
            dcc.DatePickerRange(id='my_date_picker',
                                min_date_allowed=datetime(2000,1,1),
                                max_date_allowed=datetime.today(),
                                start_date=datetime(2018,1,1),
                                end_date=datetime.today())
            ], style={'display':'inline-block'}),
  html.Div([html.Button(id='submit-button',
                        n_clicks = 0,
                        children = 'Submit',
                        style = {'fontSize':24, 'marginLeft':'30px'})]),
  dcc.Graph(id='my_graph',
            figure={'data':[
                    {'x':[], 'y':[]}
                  ],'layout':{
                    'title': 'Chart Loading...'
                    }})
])

@app.callback(Output('my_graph', 'figure'),
             [Input('submit-button', 'n_clicks')],
             [State('my_stock_picker', 'value'),
              State('my_date_picker', 'start_date'),
              State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
  start = datetime.strptime(start_date[:10],'%Y-%m-%d')
  end = datetime.strptime(end_date[:10],'%Y-%m-%d')
  
  # Create a trace for each selected company
  traces = []
  for tic in stock_ticker:
    df = web.DataReader(tic,'iex',start,end)
    starting_price = df['close'][0]
    traces.append({'x':df.index, 'y':(df['close']/starting_price), 'name':tic})
  
  fig = {'data':traces,
         'layout':{'title':stock_ticker}
  }
  return fig

if __name__ == '__main__':
  app.run_server()