import pandas as pd
from pycaret.regression import *
from datetime import timedelta

data = pd.read_csv('example-input-oslo.csv')
location = 'oslo'

data['time'] = pd.to_datetime(data['time'])

# Create hour feature
data['hour'] = data['time'].dt.hour
# Create weekday feature
data['weekday'] = data['time'].dt.weekday
# Create month feature
data['month'] = data['time'].dt.month

data.dropna(subset=['consumption'], inplace=True)

regression_setup = setup(data=data, target='consumption', session_id=123,
                         numeric_features=['observed-temperature', 'hour', 'weekday', 'month'],
                         ignore_features=['forecasted-temperature'],
                         transform_target=True, data_split_shuffle=False)

model = create_model("rf")

tuned_model = tune_model(model, choose_better=True, optimize='MAE')

final_model = finalize_model(tuned_model)



number_predict_hours = 24
# The last known time from the original data
last_time = data['time'].iloc[-25]

# Generating future timestamps for the next 24 hours (the hours we want to predict)
future_timestamps = [last_time + timedelta(hours=i) for i in range(1, number_predict_hours + 1)]

future_data = data.copy()
# Limit future data to the next 24 hours after the last known time
future_data = future_data[(future_data['time'] > last_time) & (future_data['time'] <= future_timestamps[-1])]
future_hours = future_data['time'].dt.hour
future_weekdays = future_data['time'].dt.weekday
future_months = future_data['time'].dt.month
future_forecast_temperatures = future_data['forecasted-temperature'].values

print(len(future_data))

# Creating the future_data DataFrame, which will be used for the prediction
future_data = pd.DataFrame({
    'time': future_timestamps,
    'observed-temperature': future_forecast_temperatures,
    'location': location,
    'hour': future_hours,
    'weekday': future_weekdays,
    'month': future_months
})

# Predict the consumption for the next 24 hours using the trained model
future_data['time'] = pd.to_datetime(future_data['time'])
predictions = predict_model(final_model, data=future_data)

predictions.rename(columns={'observed-temperature': 'forecasted-temperature'}, inplace=True)
predictions.rename(columns={'prediction_label': 'predicted-consumption'}, inplace=True)


print(f"\n\n\n________________PREDICTIONS FOR {future_timestamps[0]} - {future_timestamps[-1]}________________\n\n")
print(predictions)
print("_______________________________________________________________________________________________")


filename = f'predictions-{future_timestamps[0]} - {future_timestamps[-1]}.csv'
predictions.to_csv(filename, index=False)