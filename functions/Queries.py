import pandas as pd
from functions.Import_dictionaries import * 



# advanced options in kwargs:
#       unique=True --> take only unique values, no device duplicates

def ExtractData(df, column: str, option: int, **kwargs):
    """function extracting data from dataframe

    Args:
    - df (dataframe): provide full dataframe
    - column (str): attribute of dataframe
    - option (int): option to execute:
        - option 1: count each value of a column
        - option 2: count each value of a column selecting the country of interest --> pass country
        - option 3: count a single value of a column for each country  --> pass keyWord
        - option 4: select rows matching an input keyword on passed column (does not provide any count) --> pass 'keyWord'

    Returns:
        pandas series/pandas dataframe: count of values/reduced dataframe
    """
    #checking dataframe
    if df.empty:
        return df if option==4 else pd.Series()

    #first advanced options
    dataframe=df
    if 'unique' in kwargs:
        dataframe=df.drop_duplicates(subset='device_id', keep="first")

    #OPTIONS EVALUATION
    if option==1:         #option 1
        x=dataframe[column].dropna()
        return x.value_counts()

    elif option==2: 		#option 2
        x=dataframe[dataframe['country'] == dict_country(kwargs['country'])]
        x=x[column].dropna()
        return x.value_counts()

    elif option==3:		    #option 3
        indexes=dataframe[column].str.match(kwargs['keyWord'],na=False,case=False) #str.match for a strict search
        x = dataframe.country[indexes]  
        return x.value_counts()

    elif option==4:
        indexes=dataframe[column].str.match(kwargs['keyWord'],na=False)
        return dataframe.loc[indexes]


    else:
        return "error"


def countryFull(df,attr:str):
    """return countries having values in passed attr

    Args:
    - df (dataframe): pandas dataframe 
    - attr (str): column name

    Returns:
        list: list of countries
    """
    indexes=df[attr].notnull()
    return df.country[indexes].unique()

def Merge_Dates(series):
    """Merge index dates of pandas series by removing days and keeping months-years; clean outliers 

    Args:
        series (pandas series): pandas series with dates as indices

    Returns:
        list: X
        list: Y
    """
    series.rename(lambda x: x[0:7],inplace=True)
    series.sum(level=0)
    series.sort_index(inplace=True)
    to_drop=[]
    i=0
    while(series.index[i]<'1999-01-01'):
        to_drop.append(series.index[i])
        i+=1
    i=len(series)-1
    while(series.index[i]>"2021-01-01"):
        to_drop.append(series.index[i])         
        i-=1
    series.drop(to_drop,inplace=True)
    X_dates=[]
    Y_dates=[]
    for index in series.index:
        X_dates.append(index)
        Y_dates.append(series[index].sum())
    return X_dates,Y_dates