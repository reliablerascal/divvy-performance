# Divvy Bikeshare Performance
<em>This analysis of Chicago's Divvy bikeshare program measures the availability of "unlimited ride" classic bikes as well as availability of open docks.</em>

Divvy promises paid annual members (@ $131/year) ["unlimited 45-minute rides on classic bikes."](https://divvybikes.com/pricing) But when these classic (i.e. non-electric) bikes aren't available, riders have to pay $0.17 per minute to use an electric bike or else look for a classic bike at an adjacent station.

At the end of each ride, classic bike riders also rely on the availability of open docks at their intended destination station. When no docks are available, riders have to find an adjacent station further from their intended destination. This may also cause the rider to exceed the 45-minute ride limit, incurring $0.17/minute charges.

This repo acquires station status every hour, looking for the following problems at each timepoint:
<ul>
<li>no classic bikes available
<li>no open docks available
</ul>

The initial analysis looks at hourly station status on November 17, 2023. To set the stage for longer-term analysis, I've also been requesting and saving hourly data since 11/26/24 to date (currently 1/7/24). 

## Preliminary Findings for Classic Bike Availability
My key findings thus far are as follows. Of 709 classic Divvy stations:
<ul>
<li>534 stations (75%) of stations had one or more classic bikes at all times.
<li>121 stations (17%) had no classic bikes at least 15% of the time.
<li>61 stations (9%) had no classic bikes at least 30% of the time.
</ul>

To look at the geographical distribution of problematic stations, 
I [mapped the results in Flourish](https://public.flourish.studio/visualisation/15811768/).

<img src="images/Divvy Classic Bikes 2023_11_17.png">

<br>
Stations with frequent shortages of classic bikes appear to be concentrated in the Loop, the Near West Side, and the Near North Side. 
<br><br>
<img src="images/Divvy Classic Bikes 2023_11_17 downtown zoom.png">

## Data Sources

|Data Source|Description|
|---|---|
|[List of JSON Feeds](https://gbfs.lyft.com/gbfs/2.3/chi/gbfs.json)|List of all Divvy System Feeds|
|[Station Types](https://github.com/reliablerascal/divvy-performance/blob/main/data/Divvy_Station_List_11.16.23.csv) |Station Type (classic, lightweight) for all stations, as requested by FOIA S061504-112023 submitted to the Chicago Department of Transportation|
|[Vehicle Type Lookup](https://gbfs.lyft.com/gbfs/2.3/chi/en/vehicle_types.json)|Lookup table identifying vehicle_type_id 1=classic, 2=electric, 3=scooter|
|[Station Info](https://gbfs.lyft.com/gbfs/2.3/chi/en/station_information.json)|Latitude and Longitude for each station|
|[Station Status](https://gbfs.lyft.com/gbfs/2.3/chi/en/station_status.json)|# of bikes of each type available at time of API request|
|[Chicago Community Geographic Boundaries](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6)| shapefile for Chicago community areas|

## Overview of Data Pipeline
<strong>Extract</strong>- a [GitHub workflow](https://github.com/reliablerascal/divvy-performance/blob/main/.github/workflows/run.yml) initiates an API request every hour using the script [api-request.py](https://github.com/reliablerascal/divvy-performance/blob/main/scripts/api-request.py)

<strong>Transform</strong>- [api-request.py](https://github.com/reliablerascal/divvy-performance/blob/main/scripts/api-request.py) saves most fields as-is, but also extracts the following nested fields from the JSON dictionary prior to saving data:
<ul>
<li>timestamp = last_reported time for each station, converted to hours/minutes in Central Time
<li>n_classic = # of classic bikes (nested within vehicle_types_available dictionary, with vehicle_type_id = 1)
<li>n_electric = # of electric bikes (vehicle_type_id = 2)
<li>n_scooters = # of scooters (vehicle_type_id = 3)
</ul>

## Overview of Data Analysis
I used the following Jupyter Notebooks for analyzing data:

[02-prepare-dataset-for-analysis.ipynb](https://github.com/reliablerascal/divvy-performance/blob/main/notebooks/02-prepare-dataset-for-analysis.ipynb)- this accomplishes the following:
<ul>
<li>merges station info (community area, GPS location, station type) into station status data to create one analytic dataset
<li>calculates key metrics: is_no_classic and is_no_docks
<li>removes all "public racks" (i.e. non-stations)
</ul>

[03-summarize-data.ipynb](https://github.com/reliablerascal/divvy-performance/blob/main/notebooks/03-summarize-data.ipynb)
<ul>
<li>combines hourly data into one file
</ul>

## Challenges, etc.
Solved
<ul>
<li>I originally tried to request data every 15 minutes, but GitHub seemed to be unexpectedly throttling my requests. I scaled back to requesting data every hour.
<li>Initial analysis suggested a prevalence of docks with 0% classic bike availability on the northwest and southwest sides. Visiting some of these stations, I realized that most of these "problematic" stations were actually lightweight stations with no docks, only a post for tying up electric bikes. Information about <strong>station type</strong> is not provided in any of Divvy's data, but I was able to get this info via a FOIA request.
</ul>

Because the [City's open data portal](https://data.cityofchicago.org/Transportation/Divvy-Bicycle-Stations-Historical/eq45-8inv/about_data) has no station status data newer than 9/10/22, I've been requesting data via API and saving it in this repo.

## Possible Next Steps for Developing This Analysis
<ul>
<li><strong>Review the city's contracts with Lyft</strong> and their subcontracted operator, to set the stage for comparing outcomes vs. promised contractual metrics. <a href="https://comptroller.nyc.gov/newsroom/comptrollers-review-of-citi-bike-finds-worrying-decreases-in-service-reliability-under-lyfts-operation-especially-in-low-income-neighborhoods">New York City's comptroller report (November 2023)</a> seems to provide an excellent template for bikeshare accountability.
<li><strong>Analyze data over a longer time period</strong> to assess enduring trends. While it should be quick and easy to merge additional datasets, analysis would be complicated by the facts that Divvy scales back its fleet and eliminates seasonal staff over the winter (from December 1).
<li><strong>Incorporate metrics on total bike availability</strong> to show how often riders have no options (i.e. no electric bikes AND no classic bikes) vs. no affordable options.
<li><strong>Summarize bike availability by community area</s
trong>.
<li><strong>Data pipeline improvements</strong>
    <ul><li>Automate data transformations and calculations</strong> to facilitate long-term analysis. This should only be done once the process and accountability metrics are firmly established.<li><strong>Minor adjustments to timestamp tracking</strong>- 1) revise timestamp in filename suffix to 24-hour format (i.e. 13:00 vs. 1 PM) to facilitate sorting in visual interfaces, 2) record timestamp as time_reported, and determine time_retrieved during request
 </ul>
 </ul>

 ## Guide to the Repository
 
This repository is organized into the following folders:
* [data](data/)- static station info (GPS, station type), as well as hourly station status requested by API
* [notebooks](notebooks)- Python code for data exploration, development of data acquisition script, and data transformation
* [results](results/)- Data analysis summaries
* [scripts](scripts/)- includes api-request.py, the script run each hour to extract data from Divvy's API and transform it for analysis