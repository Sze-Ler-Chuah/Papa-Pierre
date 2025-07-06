from __future__ import annotations
from locations import City, Country, test_example_countries_and_cities
import re

def create_cities_countries_from_CSV(path_to_csv: str) -> None:
	"""
	Reads a CSV file given its path and creates instances of City and Country for each line.
	"""
	with open(path_to_csv,"r") as line:
		header = line.readline().strip('\n').split(',') #remove the trailing "\n", split into a list by ","
		#store the index of certain columns based on its headers to the corresponding variables
		for col_name in header:
			#col_name is converted to lower case before comparing to ensure non case-sensitive
			if col_name.lower()== 'city_ascii':
				city_ascii=header.index('city_ascii')
			elif col_name.lower()== 'lat':
				lat = header.index('lat')
			elif col_name.lower()== 'lng':
				lng = header.index('lng')
			elif col_name.lower()== 'country':
				country = header.index('country')
			elif col_name.lower()== 'iso3':
				iso3 = header.index('iso3')
			elif col_name.lower()== 'capital':
				capital = header.index('capital')
			elif col_name.lower()== 'id':
				ID = header.index('id')
		#iterate through each line in the csv file
		for F_row in line:
			F_row = F_row.strip('\n').split(',')  #remove the trailing "\n" of each row except header, split into a list by ","
			#To encounter special cases which have ",(s)" inside the column that had to be joined back, ensure all rows have the same number of columns
			i=False #indicate whether special cases have been encountered
			row=[]  #list to store the columns of each row after organizing
			for x in F_row:
				y=[]    #list to store the elements of the columns which contain ",(s)"
				#case for the first element of special column
				if '"' in x and not i:
					y.append(x)
					i=True  #the first element of special column has been found
				#case for the last element of special column
				elif '"' in x and i:
					y.append(x)
					y=''.join(y)    #join all elements of the column
					row.append(y)   #append the complete column back to row
					i=False #the last element of special column, reset i to False
				#case for the intermediate element(s) of special column
				elif i:
					y.append(x)
				#case for normal columns
				else:
					row.append(x)
			#To create only one country objects for every countries, avoid duplication
			if row[country] not in Country.countries.keys(): #country name is used to compute
				Country(row[country],row[iso3])
			City(row[city_ascii],row[lat],row[lng],row[country],row[capital],row[ID])   #create city objects for every rows with corresponding values

if __name__ == "__main__":
	create_cities_countries_from_CSV("worldcities_truncated.csv")
	test_example_countries_and_cities()

