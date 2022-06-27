# Project Proposal

## Question:
The project will map property sales in the last ~120 days in the 100 largest US cities. In addition, a few summary statistics for each location (e.g. average sale price, average cost per square foot, etc.) will be displayed for the relevant time period. The system could be beneficial for economists, city planners, or anyone looking to better understand recent trends in the housing market.

## Data Description:
Data will be pulled from an API, [Realty in the US](https://rapidapi.com/apidojo/api/realty-in-us/). I plan to set up a nightly automatic refresh of the data using Airflow. A unit of analysis is a home sold in one of the top 100 US cities by population. Example data points include
* Address
* Sale Price
* Date Sold
* Square Feet
* Bedrooms
* Bathrooms
* Latitude
* Longitude

From this data, we can calculate summary statistics over a specific time frame for each city to be part of the map visualization. Approximately 500,000 records will be stored initially but, ideally, new property sales are appended to old ones so the data points will grow over time. The scope of data will be set by the limits of the API above and, in some cases, may not offer a complete set of home sales.

## Tools:
I will set up an automatic data ingestion from the API above to a MongoDB database to store relevant JSON files (and Airflow for scheduled ingestion). Data cleaning and processing will be done with Python and Spark. Appropriate tests will be incorporated. I will create a geovisualization app using Flask and Mapbox. The web app will be hosted with Heroku. 

## MVP Goal:

An MVP will include a local web app with a map visualization that pulls relevant home sales data from a flat file for one major city.

## Pipeline sketch:
<img width="783" alt="image" src="https://user-images.githubusercontent.com/5652437/175840231-f4942abf-c6eb-4895-8adc-61814a2e7eb6.png">

