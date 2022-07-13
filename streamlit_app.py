import streamlit as st
import pandas as pd
import pymongo
import json
import geopandas as gpd
import plotly.express as px
#from get_zip_code_shape_files import get_shape_files
from get_api_data import get_mongo

three_month_avg_city = pd.read_csv("three_month_avg_city.csv")
three_month_avg_city_zip = pd.read_csv("three_month_avg_city_zip.csv")
three_month_avg_city_timeseries = pd.read_csv("three_month_avg_city_timeseries.csv")
shape_file_data = gpd.read_file("geo_data.json").set_index("ZCTA5CE10")

st.set_page_config(layout="wide")

st.subheader('Need new data?')
new_data = st.button("Update")

# Select which city to display 
st.title('Average (Median) Saleprice of Homes in Major US CIties')
city_select = st.selectbox(
     'Choose metro area',
    list(three_month_avg_city["metro_area"].unique()),
    )

three_month_avg_city_zip_show = three_month_avg_city_zip[three_month_avg_city_zip["metro_area"]==city_select]
#zip_list = three_month_avg_city_zip_show["postal_code"].apply(lambda x: int(x)).unique()
#updated_shape_file_data = shape_file_data[shape_file_data["ZCTA5CE10"].astype(int).isin(zip_list)].set_index("ZCTA5CE10")

c1, c2, c3 = st.columns((2,1, 1))

# Show map with average sale price per zip code
fig = px.choropleth(three_month_avg_city_zip_show, geojson=shape_file_data, locations='postal_code', color='median_sale_price',
                           color_continuous_scale="Viridis",
                           #range_color=(0, 420000),
                           #mapbox_style="carto-positron",
                           #zoom=5, 
                           #center = {"lat": 41.5, "lon": -81.6},
                           #opacity=0.5,
                           scope = "usa",
                           labels={'median_sale_price':'3-Month Avg. Sale Price'}
                          )
fig.update_geos(fitbounds="locations")
c1.plotly_chart(fig)

# Show average price over the past 3 months for the metro area
three_month_avg_city_timeseries_show = three_month_avg_city_timeseries[three_month_avg_city_timeseries["metro_area"]==city_select]
price_over_time = px.line(three_month_avg_city_timeseries_show, x="month_name", y="median_sale_price", title='Median Price of Sold Homes')
c2.plotly_chart(price_over_time, use_container_width=True)

# Show raw data for each zip 
c3.subheader('Raw data')
c3.write(three_month_avg_city)


