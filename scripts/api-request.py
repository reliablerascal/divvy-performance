import pandas as pd
import requests
import datetime
import pytz

ident = (
	"Rob Reid (reliablerascal@gmail.com), " +
	"journalist for the public interest retrieving station status data over a short period of time"
)

url = f"https://gbfs.lyft.com/gbfs/2.3/chi/en/station_status.json?"
response = requests.get(url, headers= {
"From": ident
})
data = response.json()
response
print("requesting data from Divvy API")

# get timestamp of dataset for filename
central_tz = pytz.timezone('America/Chicago')
status_timestamp = datetime.datetime.utcfromtimestamp(data['last_updated']).replace(tzinfo=pytz.utc)
status_timestamp = status_timestamp.astimezone(central_tz).strftime('%Y_%m_%d_%I%M%p')

#############
# PREP DATA
#############

#read into dataframe and rename columns
df_station_status= pd.DataFrame(data['data']['stations'])

# get timestamp for each station (which might be different from the dataset timestamp)
central_tz = pytz.timezone('America/Chicago')
df_station_status['timestamp'] = pd.to_datetime(df_station_status['last_reported'], unit='s', utc=True)
df_station_status['timestamp'] = df_station_status['timestamp'].dt.tz_convert(central_tz)
df_station_status['timestamp'] = df_station_status['timestamp'].dt.strftime('%m/%d/%Y %I:%M %p')

# pull out JSON fields
df_station_status['n_classic'] = df_station_status['vehicle_types_available'].apply(
    lambda x: next((item['count'] for item in x if item['vehicle_type_id'] == '1'), 0))
df_station_status['n_electric'] = df_station_status['vehicle_types_available'].apply(
    lambda x: next((item['count'] for item in x if item['vehicle_type_id'] == '2'), 0))
df_station_status['n_scooters'] = df_station_status['vehicle_types_available'].apply(
    lambda x: next((item['count'] for item in x if item['vehicle_type_id'] == '3'), 0))

#remove unneeded fields
df_station_status = df_station_status.drop(
    columns=['vehicle_docks_available','last_reported','vehicle_types_available'],axis=1)

filename = f"data/station_status_{status_timestamp}.csv"
df_station_status.to_csv(filename, index=False)
print(f"saving data as '{filename}'")