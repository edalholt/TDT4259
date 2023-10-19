import requests
import json
import csv
from datetime import datetime, timedelta


trondheim = '1-211102'
oslo = '1-72837'
stavanger = '1-15183'
bergen = '1-92416'
tromso = '1-305409'

locationId = oslo  # Change this to your desired location ID

startDate = '2022-04-07'
endDate = '2023-04-02'

# Convert the start and end date strings to datetime objects
start_date_obj = datetime.strptime(startDate, '%Y-%m-%d')
end_date_obj = datetime.strptime(endDate, '%Y-%m-%d')

days = []

# Iterate through the date range
current_date = start_date_obj
while current_date <= end_date_obj:
    # Format the current date as a string
    current_date_str = current_date.strftime('%Y-%m-%d')

    # Make the request for the current date
    url = f'https://www.yr.no/api/v0/locations/{locationId}/observations/{current_date_str}'
    response = requests.get(url)

    data = response.text
    parse_json = json.loads(data)
    try:
        data = parse_json['historical']['days'][0]['hours']

        daily_data = []

        for hour in data:
            day = {
                'timestamp': hour['time'],
                'min_temp': hour['temperature'].get('min', None),
                'max_temp': hour['temperature'].get('max', None),
                'avg_temp': hour['temperature'].get('value', None),
                'wind_max_gust': hour['wind'].get('maxGust', 0),
                'wind_mean_speed': hour['wind'].get('meanSpeed', 0),
                'precipitation': hour['precipitation'].get('total', 0),
            }
            daily_data.append(day)

        # Append the response to the list
        days.append(daily_data)
        print(f'Fetched data for {current_date_str} successfully')

        # Move to the next date
        current_date += timedelta(days=1)
    except:
        print(f'No data found for {current_date_str}')
        current_date += timedelta(days=1)
        continue


# Define the output CSV file name
output_csv_file = 'weather_data.csv'

# Define the CSV fieldnames based on your dictionary keys
fieldnames = ['timestamp', 'min_temp', 'max_temp', 'avg_temp',
              'wind_max_gust', 'wind_mean_speed', 'precipitation']

# Initialize a flag to indicate whether to write the header row
write_header = True

# Open the CSV file for writing
with open(output_csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Iterate through the list of daily data
    for daily_data in days:
        # Write the header row only once
        if write_header:
            writer.writeheader()
            write_header = False

        # Write the data rows for the current day
        for hour_data in daily_data:
            writer.writerow(hour_data)

print(f'Data has been written to {output_csv_file}')
