import streamlit as st
import pandas as pd
import json
import geopandas as gpd
import plotly.express as px
from datetime import date
from dateutil.relativedelta import relativedelta

month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

def clean_housing_data(df):
	df["postal_code"] =df["address"].apply(lambda x: x["postal_code"])
	df["last_update"] = pd.to_datetime(df["last_update"],utc=True)
	df["last_update_date"] = pd.to_datetime(df["last_update"]).dt.date
	df["last_update_month"] = df["last_update"].dt.month
	df["last_update_year"] = df["last_update"].dt.year
	return df

def get_housing_data():
	# housing data in JSON format {"city1":[{"key":"value"},{"key":"value"}...],"city2":[{"key":"value"},{"key":"value"}...]}
	f=open("cleveland_homes.txt")
	cities = json.load(f)
	f.close()
	df = pd.DataFrame()
	for c in cities:
		temp_df = pd.DataFrame(cities[c])
		temp_df["city"] = c
		df = df.append(temp_df)
	df = clean_housing_data(df)
	return df

def filter_past_x_months(df,x):
	x_months_past =  df[df["last_update_date"]>(date.today() + relativedelta(months=-x))]
	return x_months_past

def get_price_avg(df,column_groups):
	three_months_past =  df[df["last_update_date"]>(date.today() + relativedelta(months=-3))]
	three_month_avg = three_months_past.groupby(column_groups)["price"].median().reset_index()
	return three_month_avg

def get_relevant_shape_files(zip_list):
	polygons = gpd.read_file('https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/oh_ohio_zip_codes_geo.min.json')
	return polygons[polygons["ZCTA5CE10"].astype(int).isin(zip_list)].set_index("ZCTA5CE10")

city_data = get_housing_data()
past_three_months = filter_past_x_months(city_data,3)
past_three_months["month_name"] = past_three_months["last_update_month"].apply(lambda x: month_labels[x]) + past_three_months["last_update_year"].apply(lambda x: str(x))
three_month_overall_avg = get_price_avg(past_three_months,["city","last_update_month","month_name"])
three_month_zip_avg = get_price_avg(past_three_months,["city","postal_code"])

relevant_zips = three_month_zip_avg["postal_code"].apply(lambda x: int(x)).unique()
polygons = get_relevant_shape_files(relevant_zips)


st.set_page_config(layout="wide")

st.subheader('Need new data?')
new_data = st.button("Update")

# Select which city to display 
st.title('Average (Median) Saleprice of Homes in Major US CIties')
city_select = st.selectbox(
     'Choose metro area',
    list(city_data["city"].unique()),
    )

c1, c2, c3 = st.columns((2,1, 1))

# Show map with average sale price per zip code
three_month_zip_avg = three_month_zip_avg[three_month_zip_avg["city"]==city_select]
fig = px.choropleth_mapbox(three_month_zip_avg, geojson=polygons, locations='postal_code', color='price',
                           color_continuous_scale="Viridis",
                           range_color=(0, 420000),
                           mapbox_style="carto-positron",
                           zoom=8, center = {"lat": 41.5, "lon": -81.6},
                           opacity=0.5,
                           labels={'price':'3-Month Avg. Sale Price'}
                          )
c1.plotly_chart(fig)

# Show average price over the past 3 months for the metro area
price_over_time = px.line(three_month_overall_avg, x="month_name", y="price", title='Median Price of Sold Homes')
c2.plotly_chart(price_over_time, use_container_width=True)

# Show raw data for each zip 
c3.subheader('Raw data')
c3.write(three_month_zip_avg)


