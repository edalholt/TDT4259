import numpy as np
import matplotlib.pyplot as plt
import csv

timestamps = []
min_temps = []
max_temps = []
aneo_values = []

with open('trondheim-merge.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        timestamp = row['timestamp']
        min_temp = row['min_temp']
        max_temp = row['max_temp']
        aneo = row['Aneo']

        if min_temp and max_temp and aneo and min_temp.replace(".", "").isdigit() and max_temp.replace(".", "").isdigit() and aneo.replace(".", "").replace("−", "-").isdigit():
            timestamps.append(timestamp)
            min_temps.append(float(min_temp))
            max_temps.append(float(max_temp))
            aneo_values.append(float(aneo))

# Slice the first 100 data points
num_points_to_plot = 5000
sampled_timestamps = timestamps[num_points_to_plot-100:num_points_to_plot]
sampled_min_temps = min_temps[num_points_to_plot-100:num_points_to_plot]
sampled_max_temps = max_temps[num_points_to_plot-100:num_points_to_plot]
sampled_aneo_values = aneo_values[num_points_to_plot-100:num_points_to_plot]

plt.figure(figsize=(12, 6))
plt.plot(sampled_timestamps, sampled_min_temps,
         label='Min Temp', marker='o', alpha=0.7)
plt.plot(sampled_timestamps, sampled_max_temps,
         label='Max Temp', marker='o', alpha=0.7)
plt.plot(sampled_timestamps, sampled_aneo_values,
         label='Aneo', marker='o', alpha=0.7)

plt.xlabel('Timestamp')
plt.ylabel('Values')
plt.title('Min Temp, Max Temp, and Aneo Over Time (First 100 Rows)')

# Set x-axis ticks to display only the first and last timestamps
plt.xticks([sampled_timestamps[0], sampled_timestamps[-1]],
           [sampled_timestamps[0], sampled_timestamps[-1]])

plt.legend()

plt.tight_layout()
plt.show()
