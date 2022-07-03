import requests
import pandas as pd
from pymongo import MongoClient
from config import rapid_api_key
client = MongoClient()

url = "https://realty-in-us.p.rapidapi.com/properties/v2/list-sold"
headers = {
	"X-RapidAPI-Key": rapid_api_key,
	"X-RapidAPI-Host": "realty-in-us.p.rapidapi.com"
}

big_us_cities = pd.read_csv("biggest_us_cities.csv", header=None, names=["City","State"])
state_codes = pd.read_csv("state_codes.csv")
city_housing_sold_count = []

def get_state_code(state_name):
	return state_codes[state_codes["State"]==state_name]["Code"].item()

def get_count_housing_records(city, state):
	state_code = get_state_code(state)
	#print(state_code)
	querystring = {"city":city,"state_code":state_code,"offset":0,"limit":10,"sort":"sold_date"}
	#print(querystring)
	response = requests.request("GET", url, headers=headers, params=querystring).json()        
	#print(response)
	all_items = response["meta"]["matching_rows"]
	return all_items

def get_all_housing_records(city,state):
	querystring = {"city":city,"state_code":state,"offset":0,"limit":1}
	response = requests.request("GET", url, headers=headers, params=querystring).json()       
	total_records = response["meta"]["matching_rows"]
	limit=200
	max_offset = int(total_records/limit)
	all_items = []
	for i in range(0, max_offset+1):
		offset = i*limit
		if ((i+1)*limit)>total_records:
			limit = total_records%limit
		querystring = {"city":city,"state_code":state,"offset":offset,"limit":limit,"sort":"sold_date"}             
		response = requests.request("GET", url, headers=headers, params=querystring).json()        
		all_items = all_items+response["properties"]
	return all_items

def main():
	#big_us_cities["total_sold_records"] = big_us_cities.apply(lambda row: get_count_housing_records(row["City"],row["State"]),axis=1)
	test_cleveland = get_all_housing_records("Cleveland","OH")
	client = MongoClient()
	properties = client.properties
	properties.insert_many(test_cleveland)
	list(properties.aggregate([{'$group':{'_id':'$address.postal_code','count':{'$sum':1}}}]))
	list(properties.aggregate([{'$group':{'_id':'$address.postal_code','average':{'$avg':"$price"}}}]))

if __name__== '__main__':
	main()

