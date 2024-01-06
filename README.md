# Divvy Bikeshare Performance
<em>This analysis of Chicago's Divvy biksehare looks at availability of "unlimited ride" classic bikes, as well as open docks.</em>

The Divvy program promises paid annual members (@ $131/year) "unlimited 45-minute rides on classic bikes." But these classic (i.e. non-electric) bikes are not always available, and riders don't necessarily want to pay $0.17 per minute to use an electric bike.

Related, Divvy stations sometimes fill up, preventing riders from docking bikes at their intended destination.

This respository builds a foundation for analyzing Divvy's performance based on current station status data, considering the following metrics for each station:
<ul>
<li>one or more classic bikes available
<li>one or more open docks
</ul>

Because the [City's open data portal](https://data.cityofchicago.org/Transportation/Divvy-Bicycle-Stations-Historical/eq45-8inv/about_data) has no station status data newer than 9/10/22, I've been requesting data via API and saving it in this repo.

The initial analysis looks at hourly station status data November 17, 2023. To set the stage for longer-term analysis, I've been requesting and saving hourly data since 11/26/24 to date (currently 1/6/24). 

## Preliminary Findings
My key findings thus far are as follows:
<ul>
<li>Most stations (PROVIDE A FIGURE) had one or more classic bike at all times.
<li>A significant number of stations (PROVIDE A FIGURE)
<li>XX stations had no available classic bikes at least 30% of the time.
<li>XX of those stations are near downtown- in the Near North Side, Near West Side, or Loop.
</ul>

I [mapped the results in Flourish](https://public.flourish.studio/visualisation/15811768/).

Attempted embed- FAIL <div class="flourish-embed flourish-map" data-src="visualisation/15811768"><script src="https://public.flourish.studio/resources/embed.js"></script></div>

Exported map <img src="images/Divvy Classic Bikes 2023_11_17.png">


## Data Sources

|Data Source|Description|
|---|---|
|[List of JSON Feeds](https://gbfs.lyft.com/gbfs/2.3/chi/gbfs.json)|List of all Divvy System Feeds|
|[Station Types](https://github.com/reliablerascal/divvy-performance/blob/main/data/Divvy_Station_List_11.16.23.csv) |Station Type (classic, lightweight) for all stations, as requested by FOIA S061504-112023 submitted to the Chicago Department of Transportation|
|[Vehicle Type Lookup](https://gbfs.lyft.com/gbfs/2.3/chi/en/vehicle_types.json)|Lookup table identifying vehicle_type_id 1=classic, 2=electric, 3=scooter|
|[Station Info](https://gbfs.lyft.com/gbfs/2.3/chi/en/station_information.json)|Latitude and Longitude for each station|
|[Station Status](https://gbfs.lyft.com/gbfs/2.3/chi/en/station_status.json)|# of bikes of each type available at time of API request|
|[Chicago Community Geographic Boundaries](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6)| shapefile for Chicago community areas|

## Overview of Data Analysis Process



## Challenges, etc.
GitHub throttling
classic vs. lightweight stations. initial findings
complicating factors- 11/30 downscaled staff
fleet change in winter


## Next Steps for Developing This Analysis
<ul>
<li>analyze data over a longer time period to assess enduring trends
<li>review the city's contracts with Lyft and their subcontracted operator, to set the stage for comparing outcomes vs. promised metrics
</ul>

minor adjustments to code
<ul>
<li>revise timestamp in filename suffix to 24-hour format to facilitate sorting in visual interfaces
<li>record timestamp as time_reported, and determine time_retrieved during request
<li>adjust downstream notebooks accordingly
 </ul>

 ## Guide to the Repository
 
 Most data for this project is collected directly in Python via API.
* [data](data/)- static station info (GPS, station type), as well as hourly station status requested by API
* [notebooks](notebooks)- Python code for data exploration and development of data acquisition & transformation scripts
* [results](results/)- Data analysis summaries
* [scripts](scripts/)- includes api-request.py, the script run each hour to extract data from Divvy's API and transform it for analysis