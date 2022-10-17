import pandas as pd
import os
from functions.Import_dictionaries import *

pathfileData = os.path.dirname(__file__) + '/../data/'
df = pd.read_csv(pathfileData+ 'result.csv', low_memory= False)
df['Continent']=dict_continents(df['country'])

#dropdowns init
countries=get_keys(df['country'].unique()) #list of all countries
countries_All=["all countries"]+countries #list of all countries + 'all countries' possibility
years=['All-time','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999']

#search init
Search_Query=""
titlePage=""
devices=df[['name','device_id']].dropna().drop_duplicates()
med_field=df["medical_field"].dropna().unique()
dev_type=df["device_type"].dropna().unique()
manufacturer=df["name_manufacturer"].dropna().unique()
pageCount=0 #used in devices page to show 15 devices each time 

#init papers
#favPapers=pd.read_csv(pathfileData+ 'papers/favourites.csv', low_memory= False)
dev_type_selected=""
tmpPapers=""    #used to load csv file when papers page is open