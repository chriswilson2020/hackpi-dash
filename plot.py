import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to list all CSV files in the directory
def list_csv_files():
    return [f for f in os.listdir('.') if f.endswith('.csv')]

# Load the selected CSV file
def load_data(file_name):
    df = pd.read_csv(file_name)
    
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
    html.H1(children='Sensor Data Dashboard'),

    # Dropdown to select the CSV file
    dcc.Dropdown(
        id='file-dropdown',
        options=[{'label': f, 'value': f} for f in list_csv_files()],
        value=list_csv_files()[0],  # Set default value to the first CSV file
        clearable=False
    ),

    # Plots
    dcc.Graph(id='temperature-graph'),
    dcc.Graph(id='humidity-graph'),
    dcc.Graph(id='co2-graph'),
    dcc.Graph(id='pm-graph'),
    dcc.Graph(id='voc-graph'),
    dcc.Graph(id='nox-graph')
])

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
