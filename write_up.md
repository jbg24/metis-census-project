### Final Write-Up

## Abstract:
The goal of this project was to create an interactive web application that displays the value of sold home prices in major metro areas in the US. Using an API call, property sales from the past 3 months are retrieved from a sample of the country's largest US cities. Summary statistics for each location (i.e. the median sold home price by month and by zip code) are displayed for the relevant time period. The system is potentially beneficial for economists, city planners, or anyone looking to better understand recent trends in the housing market.

## Design:

This application uses data pulled from the [Realty in the US](https://rapidapi.com/apidojo/api/realty-in-us/) API. The API provides up-to-date information on housing in the US, including an endpoint of various features of recently sold homes. I feed in the relevant cities to the API and send the data with minimal processing to a pre-defined database in MongoDB Atlas. I process the data by reading from MongoDB, conduct analysis using Pandas, and then write CSV files to be read in by the Streamlit app. The app then offers visualizations, charts, and summary data for each city's sold homes. 

## Data:
I pull data from the "properties/v2/list-sold" endpoint as part of the API listed above. A DAG file was created to potentially create new CSV files each week using Airflow. This is not part of the existing hosted web application, however. A unit of analysis is a home sold in one of the US metro areas under consideration. The data points I store in Mongo include
* Address (including Zip Code)
* Sale Price
* Date Sold ("last_update")
* List Date

## Algorithms
I calculate the average (median) price of sold homes over the past three months from the time the data is collected. I look at the same statistic across that entire time span for each metro's zip code. Given the size of the data (<500,000), I use Pandas for all calcualtions which are fairly straightforward. 

## Tools:
* Requests, JSON, and Async for data aquisition
* Airflow for regular data updates
* Pymongo and MongoDB Atlas
* Pandas for data processing
* Streamlit and Streamlit hosting
* Plotly for streamlit graphics

## Communication
[Final presentation summary with updated data pipeline](https://github.com/jbg24/metis-homesale-project/blob/main/final_presentation.pdf)

[Live web app
](https://jbg24-metis-homesale-project-streamlit-app-2nhjq0.streamlitapp.com/)

