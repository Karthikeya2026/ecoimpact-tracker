import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_emission_trend(user_data):
    df = pd.DataFrame(user_data)
    fig = px.line(df, x='date', y='emissions', title='Your Carbon Emission Trend', labels={'emissions': 'CO2 (kg)'})
    fig.update_layout(template='plotly_dark')
    return fig.to_html(full_html=False)

def plot_category_breakdown(energy_kwh, miles_driven, waste_kg):
    factors = pd.read_csv(r'data/emission_factors.csv')

    data = {
        'Category': ['Energy', 'Travel', 'Waste'],
        'Emissions': [
            energy_kwh * factors.loc[factors['type'] == 'electricity', 'co2_kg'].values[0],
            miles_driven * factors.loc[factors['type'] == 'car', 'co2_kg'].values[0],
            waste_kg * factors.loc[factors['type'] == 'waste', 'co2_kg'].values[0]
        ]
    }
    df = pd.DataFrame(data)
    fig = px.pie(df, values='Emissions', names='Category', title='Emission Breakdown by Category')
    fig.update_layout(template='plotly_dark')
    return fig.to_html(full_html=False)