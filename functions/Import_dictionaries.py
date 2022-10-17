import ast
import os

def dict_country(Country):
	pathfile = os.path.dirname(__file__) + '/../dictionaries/country_dict.txt'
	file = open(pathfile, "r")
	contents = file.read()
	load_dict = ast.literal_eval(contents)
	name = load_dict[Country]
	file.close()
	return name

def dict_continents(countries):
	pathfile = os.path.dirname(__file__) + '/../dictionaries/continent_dict.txt'
	file = open(pathfile, "r")
	contents = file.read()
	load_dict = ast.literal_eval(contents)
	Fvector=[]
	for country in countries:
		if country!=country:
			Fvector.append("NaN")
		else:
			Fvector.append(load_dict[country])
	file.close()
	return Fvector

# function to return key for any value 
def get_keys(input): 
	pathfile = os.path.dirname(__file__) + '/../dictionaries/country_dict.txt'
	file = open(pathfile, "r")
	contents = file.read()
	load_dict = ast.literal_eval(contents)
	if type(input) == str:
			for key, value in load_dict.items():
				if input == value:
					file.close()
					return key
	else:
		Fvector=[]
		for country in input:
			for key, value in load_dict.items():
				if country == value:
					Fvector.append(key)
		file.close()
		return Fvector
	
