import requests
import pymongo
import streamlit as st
from urllib.parse import quote
import aiohttp
import asyncio
import time
import pandas as pd
from config import rapid_api_key

headers = {
	"X-RapidAPI-Key": rapid_api_key,
	"X-RapidAPI-Host": "realty-in-us.p.rapidapi.com"
}

# Relevant fields for proeperty data
property_fields = ["property_id","last_update","address","price","list_date"]

# Pull in relevant cities to get housing data for
big_us_cities = pd.read_csv("biggest_us_cities_by_pop.csv", header=None, names=["City","State"])
state_codes = pd.read_csv("state_codes.csv")
city_housing_sold_count = []

# connect to mongo db
def get_mongo():
	user = quote(st.secrets["db_username"])
	passw = quote(st.secrets["db_password"])
	client = pymongo.MongoClient(f"mongodb+srv://{user}:{passw}@cluster0.3rqxp.mongodb.net/?retryWrites=true&w=majority")
	return client[ "housing" ]

# match state name with state code
def get_state_code(state_name):
	return state_codes[state_codes["State"]==state_name]["Code"].item()

# Make API call and return list of properties 
async def get_properties(session, url, db, metro_area):
	async with session.get(url) as resp:
		prop_data = await resp.json()
		if "properties" in prop_data and len(prop_data['properties'])>0:
			properties = prop_data['properties']
			properties_subset = []
			for house in properties:
				house_subset = {}
				for k in property_fields:
					if k in house:
						house_subset[k] = house[k]
				house_subset["metro_area"] = metro_area
				properties_subset.append(house_subset)
			db.insert_many(properties_subset)
			return True
		else:
			print(prop_data)
			return None

# Using async, paginate through total records for each city and state
async def main(db,city,state):

    metro_area = f"{city},{state}"
    print(f"\nGetting sold housing data for {city}",end =" ")

    async with aiohttp.ClientSession(headers=headers) as session:
        
        tasks = []
        offset=0
        total_records = 5000

        while offset < total_records:
            if offset%1000 == 0:
            	print("...", end=" ")
            url = f"https://realty-in-us.p.rapidapi.com/properties/v2/list-sold?offset={offset}&limit=200&city={quote(city)}&state_code={state}&sort=sold_date"
            attempt = asyncio.ensure_future(get_properties(session, url, db,metro_area))
            if attempt:
            	tasks.append(attempt)
            else:
            	break
            offset = offset+200
            await asyncio.sleep(0.25)

        await asyncio.gather(*tasks)

if __name__== '__main__':
	m = get_mongo()
	sold_properties = m["sold_properties"]
	sold_properties.delete_many({})
	big_us_cities.head(50).apply(lambda x: asyncio.run(main(sold_properties, x["City"],get_state_code(x["State"]))),axis=1)




