import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime

# Initialize the app
app = dash.Dash()

# Define the layout of the app
app.layout = html.Div([
  html.H1('Interactive Stock Ticker Chart'),
  html.Div([html.H3('Enter a stock symbol:', style={'paddingRight':'30px'}),
            dcc.Input(id='my_stock_picker', value='TSLA', style={'fontSize':24, 'width':75})
            ], style={'display':'inline-block', 'verticalAlign':'top'}),
  html.Div([html.H3('Select a start and end date:'),
            dcc.DatePickerRange(id='my_date_picker',
                                min_date_allowed=datetime(2000,1,1),
                                max_date_allowed=datetime.today(),
                                start_date=datetime(2018,1,1),
                                end_date=datetime.today())
            ], style={'display':'inline-block'}),
  dcc.Graph(id='my_graph',
            figure={'data':[
                    {'x':[1,2], 'y':[3,1]}
                  ],'layout':{
                    'title': 'Default Title'
                    }})
])

@app.callback(Output('my_graph', 'figure'),
             [Input('my_stock_picker', 'value'),
              Input('my_date_picker', 'start_date'),
              Input('my_date_picker', 'end_date')])
def update_graph(stock_ticker, start_date, end_date):
  start = datetime.strptime(start_date[:10],'%Y-%m-%d')
  end = datetime.strptime(end_date[:10],'%Y-%m-%d')
  df = web.DataReader(stock_ticker,'iex',start,end)
  fig = {'data':[{'x':df.index, 'y':df['close']}],
         'layout':{'title':stock_ticker}
  }
  return fig

if __name__ == '__main__':
  app.run_server()