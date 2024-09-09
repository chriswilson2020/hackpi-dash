import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os
import argparse

# Parse command-line arguments for the directory containing CSV files
parser = argparse.ArgumentParser(description='Specify the directory containing CSV files.')
parser.add_argument('--csv-dir', type=str, default='.', help='Directory containing CSV files')
args = parser.parse_args()

# Directory containing CSV files
csv_dir = args.csv_dir

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to list all CSV files in the directory
def list_csv_files():
    return [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

# Load the selected CSV file
def load_data(file_name):
    file_path = os.path.join(csv_dir, file_name)
    df = pd.read_csv(file_path)
    
    # Rename PM columns to simpler names if they contain special characters
    df.rename(columns={
        'PM1.0 (µg/m³)': 'PM1.0',
        'PM2.5 (µg/m³)': 'PM2.5',
        'PM4.0 (µg/m³)': 'PM4.0',
        'PM10.0 (µg/m³)': 'PM10.0'
    }, inplace=True)
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])  # Convert to datetime
    return df

# Create the layout for the app
app.layout = html.Div(children=[
    html.H1(children='HackBerry Pi Environmental Sensor Data Web Dashboard'),

    # Dropdown to select the CSV file
    dcc.Dropdown(
        id='file-dropdown',
        clearable=False
    ),

    # Interval component to refresh data every 10 seconds
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every 10 seconds
        n_intervals=0
    ),

    # Plots
    dcc.Graph(id='temperature-graph'),
    dcc.Graph(id='humidity-graph'),
    dcc.Graph(id='co2-graph'),
    dcc.Graph(id='pm-graph'),
    dcc.Graph(id='voc-graph'),
    dcc.Graph(id='nox-graph')
])

# Callback to update the dropdown list of CSV files periodically
@app.callback(
    Output('file-dropdown', 'options'),
    [Input('interval-component', 'n_intervals')]
)
def update_dropdown(n):
    csv_files = list_csv_files()
    return [{'label': f, 'value': f} for f in csv_files]

# Callback to update the selected file in the dropdown
@app.callback(
    Output('file-dropdown', 'value'),
    [Input('file-dropdown', 'options')],
    [Input('interval-component', 'n_intervals')]
)
def set_default_file(options, n):
    if options:
        return options[0]['value']  # Select the first CSV file as default
    return None

# Callback to update the graphs based on the selected file
@app.callback(
    [Output('temperature-graph', 'figure'),
     Output('humidity-graph', 'figure'),
     Output('co2-graph', 'figure'),
     Output('pm-graph', 'figure'),
     Output('voc-graph', 'figure'),
     Output('nox-graph', 'figure')],
    [Input('file-dropdown', 'value')]
)
def update_graphs(selected_file):
    if selected_file is None:
        return [{}] * 6  # Return empty graphs if no file is selected
    
    # Load the data for the selected file
    df = load_data(selected_file)
    
    # Create individual line plots using Plotly Express
    fig_temperature = px.line(df, x='Timestamp', y='Temperature (C)', title='Temperature Over Time')
    fig_humidity = px.line(df, x='Timestamp', y='Humidity (%)', title='Humidity Over Time')
    fig_co2 = px.line(df, x='Timestamp', y='CO2 (ppm)', title='CO2 Levels Over Time')
    fig_pm = px.line(df, x='Timestamp', y=['PM1.0', 'PM2.5', 'PM4.0', 'PM10.0'],
                     title='Particulate Matter Levels Over Time')
    fig_voc = px.line(df, x='Timestamp', y='VOC Index', title='VOC Index Over Time')
    fig_nox = px.line(df, x='Timestamp', y='NOx Index', title='NOx Index Over Time')

    return fig_temperature, fig_humidity, fig_co2, fig_pm, fig_voc, fig_nox

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
