# Project Proposal

## Question:
The project will provide an updated version of Stanford's [Income Segregation Map](https://inequality.stanford.edu/income-segregation-maps). The map offers a visualization of major US cities' level of income segregation. The map and accompanying visualizations for this project will work off of definitions and methodologies which are explained in detail by existing Stanford [research](https://cepa.stanford.edu/sites/default/files/the%20continuing%20increase%20in%20income%20segregation%20march2016.pdf). Ultimately, I will show for each US city above 500,000 people the proportion of families living in "poor" or "affluent" neighborhoods (i.e. census block groups) according to 2016-2020 and 2011-2015 American Community Survey estimates. The system could be beneficial for economists, city planners, or community organizers/advocates looking to better understand recent trends in housing segregation and income inequality.

## Data Description:
Data will be pulled from the [American Community Survey API](https://www.census.gov/data/developers/data-sets.html) provided by the US Census Bureau. Specifically, I will use [a wrapper already created](https://github.com/datamade/census). While the data source in this case does not update regularly, for learning purposes I plan to set up a daily automatic refresh of the data using Airflow. A unit of analysis is the number of families in a specific income brack in a census tract:
* GEOID (Census tract identifier)
* Income bracket (e.g. $10,000, $15,000, etc.)
* Count of families
* Year 
* 

We will also need the median family income of each Metropolitan Statistical Area under analysis for comparison:
* Metropolitan Statistical Area Identifier 
* Metro Name
* Median Family Income

A statis [reference file](https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html) will be needed to associate census tracts with MSA's.  From this data, we can calculate the percentage of families in each tract that fall into "poor" or "affluent" categories (based on Stanford definitions).  Using Dash Plotly, I will visualize the findings for each census tract, metro area, and country as a whole. In other words, from 2015 to 2020 what are the city- and country-wide trends in income segregation. 

## Tools:
I will set up an automatic data ingestion from the census API to a SQL database. Data cleaning and preprocessing will be done prior to data storage and data calculations will be made to feed data into a Dashboard created using Plotly and hosted by Heroku. What will be neeed for data handling? 

## MVP Goal:

An MVP will include a local web application with a map visualization that pulls data from a flat file for one major metropolitan area. 

## Pipeline sketch:
