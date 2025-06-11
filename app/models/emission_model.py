import pandas as pd
from sklearn.linear_model import LinearRegression
factors = pd.read_csv(r'data/emission_factors.csv')



def calculate_emissions(energy_kwh, miles_driven, waste_kg):
    energy_factor = factors.loc[factors['type'] == 'electricity', 'co2_kg'].values[0]
    travel_factor = factors.loc[factors['type'] == 'car', 'co2_kg'].values[0]
    waste_factor = factors.loc[factors['type'] == 'waste', 'co2_kg'].values[0]
    return (energy_kwh * energy_factor) + (miles_driven * travel_factor) + (waste_kg * waste_factor)

def predict_future_emissions(user_data):
    if len(user_data) < 2:
        return None
    df = pd.DataFrame(user_data)
    X = df[['energy_kwh', 'miles_driven', 'waste_kg']]
    y = df['emissions']
    model = LinearRegression().fit(X, y)
    prediction = model.predict(X.tail(1))
    return round(prediction[0], 2)