# Predicting consumption - How to

1. Provide the training data on the same format as [example-input-oslo](example-input-oslo.csv).

   - This file need to contain values (time,location,consumption,forecasted-temperature,observed-temperature)
   - The five last days of consumption could be missing
   - The last 24 hours could be missing for observed-temperature, as the last 24 timestamps should be future timestamps (the future we want to predict)

2. Rename the filename of line 5 in [forecast_24g.py](forecast_24h.py) to match the name of your input CSV.

3. Create the predictions by running `python forecast_24h.py` from this directory.
4. The predicted values should now appear in a new file named `predictions[start-time]-[end-time].csv`
