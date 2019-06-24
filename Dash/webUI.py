#########################
# Build a WebUI for the results in PostgreSQL with Dash
#########################


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import subprocess
import psycopg2
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
        "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
        "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # Banner
    html.Div(
    	html.H2('Right to be Forgotten'),
    	className = 'banner'
    ),

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

    	html.Div(
    		id = 'startLabel',
    	),

    	html.Div(
    		id = 'stopLabel'
    	)
    ]),


    # Plot the number of each device over time
    html.Div([
        html.Div([
            html.H3("Counts for Devices Over Time")
        ], className='Title'),
        html.Div([
            dcc.Graph(id='counts_plot')
        ]),
        dcc.Interval(id='updatePlot', interval=1000, n_intervals=0),
    ], className='row wind-speed-row'),

])


# Function that cleans DB in Redis and PostgreSQL, and starts Kafka producer
@app.callback(
    Output('startLabel', 'children'),
    [Input('startButton','n_clicks')]
)
def startTrading(n_clicks):
    if n_clicks and n_clicks > 0:
        subprocess.Popen('bash run.sh', shell=True)
        return 'Started Streaming'

# Function that stops Kafka producer
@app.callback(
    Output('stopLabel', 'children'),
    [Input('stopButton', 'n_clicks')]
)
def stopTrading(n_clicks):
    if n_clicks and n_clicks > 0:
        subprocess.Popen('bash stop.sh', shell=True)
        return 'Stopped Streaming.'


# Function that updates the counts_plot
@app.callback(
    Output('counts_plot', 'figure'),
    [Input('updatePlot','n_intervals')]
)
def updateGraph(n_intervals):
    connection = psycopg2.connect(host = 'ip-10-0-0-5', port = '5431', database = 'my_db', user = 'spark', password = 'spark')    
    data = pd.read_sql_query("SELECT time, counts FROM device_counts Where device = 'iPhone' Order by time;", connection)
    data = data.to_dict('records')
    
    time = []
    counts = []
    for line in data:
        time.append(line['time'])
        counts.append(line['counts'])

    trace0 = go.Scatter(
        x = time,
        y = counts,
        mode = 'lines',
        name = 'Test',
        line = dict(
            color = ('rgb(66, 196, 247)')
        )
    )
	
    layout = dict(
            xaxis = dict(title = 'Time'),
            yaxis = dict(title = 'Counts')
    )
			
    return go.Figure(data = [trace0], layout = layout)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
