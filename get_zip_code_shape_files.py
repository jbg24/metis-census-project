from github.MainClass import Github
import geopandas as gpd
import os

path = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/"
directory = 'ShapeRelevant'

g = Github()
repo = g.get_repo("OpenDataDE/State-zip-code-GeoJSON")
file_list = repo.get_contents("")

def refresh_shape_files():
	shape_files = gpd.GeoDataFrame()
	for file in file_list:
		if file.name.split(".")[-1] == "json":
			state = gpd.read_file(path+file.name)
			shape_files = pd.concat([shape_files, state], ignore_index=True)
	return shape_files

def get_shape_files():
	shape_files = gpd.GeoDataFrame()
	for file in os.listdir(directory):
		f = os.path.join(directory, file)
		if f.split(".")[-1] == "json":
			state = gpd.read_file(f)
			shape_files = shape_files.append(state)
	return shape_files
