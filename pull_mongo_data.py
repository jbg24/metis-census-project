import pymongo
from urllib.parse import quote
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import json
import streamlit as st


month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

# Initialize connection.
def init_connection():
	user = quote(st.secrets["db_username"])
	passw = quote(st.secrets["db_password"])
	return pymongo.MongoClient(f"mongodb+srv://{user}:{passw}@cluster0.3rqxp.mongodb.net/?retryWrites=true&w=majority")

client = init_connection()
db = client.housing

# Pull data from the collection.
def get_property_data():
    items = db.sold_properties.find({ "price": { '$gt': 0 } },{"metro_area":1,"price":1,"address.postal_code":1,"last_update":1,"_id":0})
    return list(items)

items = get_property_data()

# Make necessary changes to data for analysis
def clean_data(df):
	df["postal_code"] =df["address"].apply(lambda x: x["postal_code"])
	df["last_update"] = pd.to_datetime(df["last_update"],utc=True)
	df["last_update_date"] = pd.to_datetime(df["last_update"]).dt.date
	df["last_update_month"] = df["last_update"].dt.month
	df["last_update_year"] = df["last_update"].dt.year
	return df

# Get data from the past 3 months to analyze
def filter_past_x_months(df,x):
	x_months_past =  df[df["last_update_date"]>(date.today() + relativedelta(months=-x))]
	return x_months_past

# Get the average (median) price of sold homes by column group
def get_price_avg(df, column_groups):
	price_avg = df.groupby(column_groups)["price"].median().reset_index().rename(columns={"price":"median_sale_price"})
	count = df.groupby(column_groups)["price"].count().reset_index().rename(columns={"price":"house_count"})
	return price_avg.merge(count,on=column_groups)

def get_zip_code_data(df):
	geo_data = {"type":"FeatureCollection"}
	zip_code_list = df["postal_code"].unique().tolist()
	relevant_zips = list(db.zip_codes.find({"properties.ZCTA5CE10":{"$in":zip_code_list}},{"_id":0}))
	geo_data["features"] = relevant_zips
	return geo_data

def process():
	df = pd.DataFrame(items)
	df_clean = clean_data(df)
	df_past_3mo = filter_past_x_months(df_clean, 3)
	geo_data = get_zip_code_data(df_past_3mo)
	three_month_avg_city = get_price_avg(df_past_3mo, ["metro_area"])
	three_month_avg_city_zip = get_price_avg(df_past_3mo, ["metro_area","postal_code"])
	three_month_avg_city_timeseries = get_price_avg(df_past_3mo, ["metro_area","last_update_month","last_update_year"])
	three_month_avg_city_timeseries["month_name"] = three_month_avg_city_timeseries["last_update_month"].apply(lambda x: month_labels[x]) + three_month_avg_city_timeseries["last_update_year"].apply(lambda x: str(x))

	three_month_avg_city.to_csv("three_month_avg_city.csv")
	three_month_avg_city_zip.to_csv("three_month_avg_city_zip.csv")
	three_month_avg_city_timeseries.to_csv("three_month_avg_city_timeseries.csv")
	with open('geo_data.json', 'w') as outfile:
		json.dump(geo_data, outfile)

process()
