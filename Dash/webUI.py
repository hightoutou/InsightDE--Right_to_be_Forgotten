#########################
# Build a WebUI for the results in PostgreSQL with Dash
#########################


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import subprocess
import psycopg2
import pandas as pd
import yaml
import redis

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
        "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
        "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

action_types = ['view', 'click', 'submit', 'message_post']
device_types = ['iPhone', 'iPad Tablet', 'Mac Desktop', 'Android Phone', 'Windows Desktop']
deletion_rates = [('100 requests per second', 100), ('200 requests per second', 200), ('500 requests per second', 500), ('1000 requests per second', 1000)]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # Banner
    html.Div(
    	html.H1('     Right to be Forgotten'),
    	className = 'banner'
    ),

    # Choose the action_type and device_type to show
    html.Div([
    
        html.Div([
            html.Div(
                id = 'interval_1_1',
                children = '   ',
                style={'width': '48%', 'display': 'inline-block'}
            ),

            html.Div(
                id = 'interval_1_2',
                children = '   ',
                style={'width': '48%', 'display': 'inline-block', 'float': 'right'}
            ),
        ]),

        html.Div(
            html.H5('Action Type'),
            style={'width': '35%', 'display': 'inline-block'}
        ),

        html.Div(
            html.H5('Device Type'),
            style={'width': '65%', 'float': 'right', 'display': 'inline-block'}
        ),
    ]),


    html.Div([
        html.Div(
            dcc.Dropdown(
                id='action_type',
                options=[{'label': i, 'value': i} for i in action_types],
                value='view'
            ),
        style={'width': '35%', 'display': 'inline-block'}
        ),
        
        html.Div(
            dcc.Dropdown(
                id='device_type',
                options=[{'label': i, 'value': i} for i in device_types],
                value='iPhone'
            ),
            style={'width': '35%', 'display': 'inline-block'}
        )
    ]),

    html.Div([

        html.Div(
            html.H5('Deletion Request Rate'),
            #style={'width': '20%', 'display': 'inline-block'}
        ),

        html.Div(
            dcc.Dropdown(
                id='deletion_rate',
                options=[{'label': i[0], 'value': i[1]} for i in deletion_rates],
                value=100
            ),
            style={'width': '35%', 'display': 'inline-block'}
        ),

        html.Div([
            html.Div(
                id = 'interval_2_1',
                children = '   ',
                style={'width': '48%', 'display': 'inline-block'}
            ),

            html.Div(
                id = 'interval_2_2',
                children = '   ',
                style={'width': '48%', 'display': 'inline-block', 'float': 'right'}
            ),
        ])
    ]),

    # Start button and Stop button
    html.Div(children = [
    	html.Button(
    		id = 'startButton',
    		children = 'Start'
    	),

    	html.Button(
    		id = 'stopButton',
    		children = 'Stop'
    	),

        html.Button(
                id = 'clearButton',
                children = 'Clear'
        ),
        
        html.Div([
    	    html.Div(
    		id = 'start_label',
                children = '   ',
                style={'width': '20%', 'display': 'inline-block'}
    	    ),

            html.Div(
                id = 'stop_label',
                children = '   ',
                style={'width': '80%', 'float':'right', 'display': 'inline-block', 'float': 'right'}
            ),
            html.Div(
                id='clear_label',
                children = '   ',
            ) 
        ])
    ]),


    # Plot the number of each device over time
    html.Div([
        html.Div([
            dcc.Graph(id='counts_plot')
        ]),
        dcc.Interval(id='updatePlot', interval=2000, n_intervals=0),
    ], 
    className='row wind-speed-row',
    style={'width': '80%'}
    ),

    html.Div(
        id = 'deletion_count',
        children = 'Number of Deletion Requests: 0',
        style={'width': '48%', 'display': 'inline-block', 'size': 40}
    ),

])


# Function that clears DB in Redis and PostgreSQL, 
@app.callback(
    Output('clear_label', 'children'),
    [Input('clearButton','n_clicks')]
)
def clearDB(n_clicks):
    if n_clicks and n_clicks > 0:
        subprocess.Popen('bash clear_data.sh', shell=True)
        return '  ',

# Function that starts Kafka producer
@app.callback(
    Output('start_label', 'children'),
    [Input('startButton','n_clicks')], 
    [State('deletion_rate','value')]
)
def startStreaming(n_clicks, rate):
    if n_clicks and n_clicks > 0:
        subprocess.Popen('bash run_producers_sessions.sh', shell=True)
        subprocess.Popen('bash run_producers_requests.sh ' + str(rate), shell=True)
        return '  ',

# Function that stops Kafka producer
@app.callback(
    Output('stop_label', 'children'),
    [Input('stopButton', 'n_clicks')]
)
def stopSgreaming(n_clicks):
    if n_clicks and n_clicks > 0:
        subprocess.Popen('bash stop_producers.sh', shell=True)
        return '  '


# Function that updates the counts_plot
@app.callback(
    Output('counts_plot', 'figure'),
    [Input('updatePlot','n_intervals'), Input('action_type', 'value'), Input('device_type', 'value')]
)
def updateGraph(n_intervals, action, device):
    connection = psycopg2.connect(host = 'ip-10-0-0-5', port = '5431', database = 'my_db', user = config['postgres_user'], password = config['postgres_password'])    
    query = "SELECT time, elapsed_time_avg FROM device_avg_time_filter WHERE device = '"+device+"' AND action_type = '"+action+"' ORDER BY time;"
    #print(n_intervals, action, device)
    data = pd.read_sql_query(query, connection)
    data = data.to_dict('records')
    
    time = []
    avg_time = []
    for line in data:
        time.append(line['time'])
        avg_time.append(line['elapsed_time_avg']/1000)

    trace0 = go.Scatter(
        x = time,
        y = avg_time,
        mode = 'lines',
        name = 'Test',
        line = dict(
            color = ('rgb(66, 196, 247)')
        )
    )
	
    layout = dict(
        xaxis = dict(title = 'Time'),
        yaxis = dict(title = 'Average Elapsed Time(s)')
    )
    			
    return go.Figure(data = [trace0], layout = layout)


@app.callback(
    Output('deletion_count', 'children'),
    [Input('updatePlot','n_intervals')]
)
def updateDeletionCount(n_intervals):
    rdb = redis.StrictRedis(config['redis_server'], port=6379, db=0, decode_responses=True)
    cursor = '0'
    num = 0
    while cursor != 0:
        cursor, keys = rdb.scan(cursor=cursor)
        num += len(keys)
    str_return = 'Number of Deletion Requests: '+str(num)
    return str_return

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
