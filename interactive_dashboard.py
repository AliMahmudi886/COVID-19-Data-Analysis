from dash import dcc, html
import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Load preprocessed data
df = pd.read_csv('../data/covid_19_data.csv')

# Convert 'Last_Update' to datetime if it's not already
df['Last_Update'] = pd.to_datetime(df['Last_Update'])

# Calculate daily new confirmed, deaths, and recovered cases
df['Daily_Confirmed'] = df['Confirmed'].diff()
df['Daily_Deaths'] = df['Deaths'].diff()
df['Daily_Recovered'] = df['Recovered'].diff()

# Calculate mortality and recovery rates
df['Mortality_Rate'] = (df['Deaths'] / df['Confirmed']) * 100
df['Recovery_Rate'] = (df['Recovered'] / df['Confirmed']) * 100

# Calculate active cases
df['Active_Cases'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

# Calculate growth rate
df['Growth_Rate'] = df['Confirmed'].pct_change() * 100

# Initialize the Dash app
app = dash.Dash(__name__)


# Create line charts using Plotly
def create_figure(data, x_col, y_col, title):
    return px.line(data, x=x_col, y=y_col, title=title)


# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Enhanced COVID-19 Data Analysis'),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Country_Region'].unique()],
        value='Worldwide',
        clearable=False,
        style={'width': '50%'}
    ),

    dcc.Graph(id='cumulative-confirmed'),
    dcc.Graph(id='cumulative-deaths'),
    dcc.Graph(id='cumulative-recovered'),
    dcc.Graph(id='active-cases'),
    dcc.Graph(id='growth-rate'),

    dcc.Graph(id='daily-confirmed'),
    dcc.Graph(id='daily-deaths'),
    dcc.Graph(id='daily-recovered'),

    dcc.Graph(id='mortality-rate'),
    dcc.Graph(id='recovery-rate'),

    dcc.Graph(id='country-comparison')
])


@app.callback(
    [Output('cumulative-confirmed', 'figure'),
     Output('cumulative-deaths', 'figure'),
     Output('cumulative-recovered', 'figure'),
     Output('active-cases', 'figure'),
     Output('growth-rate', 'figure'),
     Output('daily-confirmed', 'figure'),
     Output('daily-deaths', 'figure'),
     Output('daily-recovered', 'figure'),
     Output('mortality-rate', 'figure'),
     Output('recovery-rate', 'figure'),
     Output('country-comparison', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_graphs(selected_country):
    if selected_country == 'Worldwide':
        filtered_df = df
    else:
        filtered_df = df[df['Country_Region'] == selected_country]

    fig_confirmed = create_figure(filtered_df, 'Last_Update', 'Confirmed',
                                  'Cumulative Confirmed COVID-19 Cases Over Time')
    fig_deaths = create_figure(filtered_df, 'Last_Update', 'Deaths', 'Cumulative Deaths Over Time')
    fig_recovered = create_figure(filtered_df, 'Last_Update', 'Recovered', 'Cumulative Recoveries Over Time')
    fig_active_cases = create_figure(filtered_df, 'Last_Update', 'Active_Cases', 'Active COVID-19 Cases Over Time')
    fig_growth_rate = create_figure(filtered_df, 'Last_Update', 'Growth_Rate', 'Growth Rate of COVID-19 Cases')

    fig_daily_confirmed = create_figure(filtered_df, 'Last_Update', 'Daily_Confirmed', 'Daily New Confirmed Cases')
    fig_daily_deaths = create_figure(filtered_df, 'Last_Update', 'Daily_Deaths', 'Daily New Deaths')
    fig_daily_recovered = create_figure(filtered_df, 'Last_Update', 'Daily_Recovered', 'Daily New Recoveries')

    fig_mortality_rate = create_figure(filtered_df, 'Last_Update', 'Mortality_Rate', 'Mortality Rate Over Time')
    fig_recovery_rate = create_figure(filtered_df, 'Last_Update', 'Recovery_Rate', 'Recovery Rate Over Time')

    country_comparison_fig = create_figure(df, 'Last_Update', 'Confirmed', 'Country/Region Comparison')
    country_comparison_fig.update_traces(mode='lines', connectgaps=True)

    return (fig_confirmed, fig_deaths, fig_recovered, fig_active_cases, fig_growth_rate,
            fig_daily_confirmed, fig_daily_deaths, fig_daily_recovered,
            fig_mortality_rate, fig_recovery_rate, country_comparison_fig)


if __name__ == '__main__':
    app.run_server(debug=True)
