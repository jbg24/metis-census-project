import streamlit as st
import pandas as pd
import pymongo
import json
import geopandas as gpd
import plotly.express as px
import pathlib
from st_aggrid import AgGrid
from datetime import datetime


three_month_avg_city = pd.read_csv("three_month_avg_city.csv")
three_month_avg_city_zip = pd.read_csv("three_month_avg_city_zip.csv")
three_month_avg_city_timeseries = pd.read_csv("three_month_avg_city_timeseries.csv")
shape_file_data = gpd.read_file("geo_data.json").set_index("ZCTA5CE10")
last_updated = datetime.fromtimestamp(pathlib.Path("three_month_avg_city.csv").stat().st_mtime)

st.set_page_config(layout="wide")

# Select which city to display 
st.title('Average (Median) Saleprice of Homes in Major US CIties')
st.write("Last updated: ", last_updated)
city_select = st.selectbox(
     'Choose metro area',
    list(three_month_avg_city["metro_area"].unique()),
    )

three_month_avg_city_zip_show = three_month_avg_city_zip[three_month_avg_city_zip["metro_area"]==city_select]
#zip_list = three_month_avg_city_zip_show["postal_code"].apply(lambda x: int(x)).unique()
#updated_shape_file_data = shape_file_data[shape_file_data["ZCTA5CE10"].astype(int).isin(zip_list)].set_index("ZCTA5CE10")

c1, c2 = st.columns((2,1))

# Show map with average sale price per zip code
fig = px.choropleth(three_month_avg_city_zip_show, geojson=shape_file_data, locations='postal_code', color='median_sale_price',
                           color_continuous_scale="Viridis",
                           #mapbox_style="carto-positron",
                           #zoom=5, 
                           #center = {"lat": 41.5, "lon": -81.6},
                           #opacity=0.5,
                           scope = "usa",
                           labels={'median_sale_price':'3-Month Avg. Sale Price'}
                          )
fig.update_geos(fitbounds="locations")
fig.update_layout(title_text = 'Median Price of Sold Homes in Past 3 Months For Metro Zip Codes')
c1.plotly_chart(fig)

# Show average price over the past 3 months for the metro area
three_month_avg_city_timeseries_show = three_month_avg_city_timeseries[three_month_avg_city_timeseries["metro_area"]==city_select]
price_over_time = px.line(three_month_avg_city_timeseries_show, x="month_name", y="median_sale_price", title='Median Price of Sold Homes',labels = {"month_name":"Month","median_sale_price":"Median Sale Price"})
c2.plotly_chart(price_over_time, use_container_width=True)

# Show raw data for each zip 
st.subheader('Raw data')
AgGrid(three_month_avg_city_timeseries[["metro_area","month_name","median_sale_price","house_count"]].rename(columns={"month_name":"MonthYear","metro_area":"Metro Area","median_sale_price":"Median 3-Month Sale Price","house_count":"No. of Sampled Homes"}))

