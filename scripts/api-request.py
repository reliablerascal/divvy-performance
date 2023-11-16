import pandas as pd
import requests
import datetime
import pytz

url = f"https://gbfs.lyft.com/gbfs/2.3/chi/en/station_status.json?"
response = requests.get(url)
data = response.json()
response
print("requesting data from Divvy API")

central_tz = pytz.timezone('America/Chicago')
status_timestamp = datetime.datetime.utcfromtimestamp(data['last_updated']).replace(tzinfo=pytz.utc)
status_timestamp = status_timestamp.astimezone(central_tz).strftime('%Y_%m_%d_%I%M%p')

df_station_status= pd.DataFrame(data['data']['stations'])
filename = f"data/station_status_{status_timestamp}.csv"
df_station_status.to_csv(filename, index=False)
print(f"saving data as '{filename}'")