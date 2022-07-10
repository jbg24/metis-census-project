import requests
import pymongo
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

# Pull in relevant cities to get housing data for
big_us_cities = pd.read_csv("biggest_us_cities_50.csv", header=None, names=["City","State"])
state_codes = pd.read_csv("state_codes.csv")
city_housing_sold_count = []

# connect to mongo db
def get_mongo():
	user = quote(st.secrets["db_username"])
	passw = quote(st.secrets["db_password"])
	client = pymongo.MongoClient(f"mongodb+srv://{user}:{passw}@cluster0.3rqxp.mongodb.net/?retryWrites=true&w=majority")
	return client[ "testdb" ]

# match state name with state code
def get_state_code(state_name):
	return state_codes[state_codes["State"]==state_name]["Code"].item()

# Make API call and return list of properties 
async def get_properties(session, url, db, metro_area):
	async with session.get(url) as resp:
		prop_data = await resp.json()
		if "properties" in prop_data:
			properties = prop_data['properties']
			for house in properties:
				house["metro_area"] = metro_area
			db.insert_many(properties)
			return True
		else:
			print(prop_data)
			return None

# Using async, paginate through total records for each city and state
async def main(db,city,state):

    metro_area = f"{city},{state}"
    print(f"Getting sold housing data for {city}...")

    async with aiohttp.ClientSession(headers=headers) as session:
        
        tasks = []
        offset=0
        total_records = 3000

        while offset < total_records:
            url = f"https://realty-in-us.p.rapidapi.com/properties/v2/list-sold?offset={offset}&limit=200&city={quote(city)}&state_code={state}"
            attempt = asyncio.ensure_future(get_properties(session, url, db,metro_area))
            if attempt:
            	tasks.append(attempt)
            else:
            	break
            offset = offset+200
            await asyncio.sleep(1/4)

        await asyncio.gather(*tasks)

if __name__== '__main__':
	m = get_mongo()
	test_col = m["testcol"]
	big_us_cities.apply(lambda x: asyncio.run(main(test_col, x["City"],get_state_code(x["State"]))),axis=1)


