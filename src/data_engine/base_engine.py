import pandas as pd
import numpy as np
"""
Engine will process data and add additional columns
"""
def compute_mean(data):
    combined_data = pd.DataFrame()
    attributes = list(data.describe().columns)
    unique_countries = data.location.unique()
    for country in unique_countries:
        data_country = data[data.location == country]
        for attr in attributes:
            mean = data_country[attr].mean()
            data_country.insert(len(data_country.columns), f'{attr} mean', mean, allow_duplicates=False) 
        combined_data = pd.concat([combined_data, data_country])
    return combined_data 

def compute_std(data):
    combined_data = pd.DataFrame()
    attributes = list(data.describe().columns)
    unique_countries = data.location.unique()
    for country in unique_countries:
        data_country = data[data.location == country]
        for attr in attributes:
            mean = data_country[attr].std()
            data_country.insert(len(data_country.columns), f'{attr} std', mean, allow_duplicates=False) 
        combined_data = pd.concat([combined_data, data_country])
    return combined_data 

def combine_data_with_mask(data, mask, attribute):
    combined_data = pd.DataFrame()
    unique_countries = data.location.unique()
    data = data.sort_values(by=["date"]).set_index("date")
    mask = mask.sort_values(by=["date"]).set_index("date")  

    for country in unique_countries:
        data_covid = data[data.location == country]
        data_mask = mask[mask.location == country]
        data_mask = data_mask.groupby(data_mask.index).first() 
         
        if data_mask.index.min() != pd.NaT and (data_covid.index.min() < data_mask.index.min()):
            country = data_mask.location.unique()
            iso_code = data_mask.iso_code.unique()
            date_range = pd.date_range(data_covid.index.min(), data_mask.index.max())
            data_mask = data_mask.resample('D').asfreq().reindex(date_range) # extending the date range
            #filling up nans of categorical data like locations country code 
            data_mask[['iso_code']] = data_mask[['iso_code']].fillna(f'{iso_code[0]}')
            data_mask[['location']] = data_mask[['location']].fillna(f'{country[0]}')
            data_mask = data_mask.fillna(0)

        data_covid[attribute] = data_mask[attribute]
        data_covid = data_covid.fillna(0)
        combined_data = pd.concat([combined_data, data_covid])
    return combined_data.reset_index()

def combine_data_with_school(data, school):
    combined_data = pd.DataFrame()
    unique_countries = data.location.unique()
    for country in unique_countries: 
        data_covid = data[data.location == country]
        data_school = school[school.location == country]
        if data_school.empty:
            school_years = 0
        else:
            school_years = data_school[data_school.columns[1]].values[0]
        data_covid[data_school.columns[1]] = school_years
        combined_data = pd.concat([combined_data, pd.DataFrame(data_covid)]) 
    return combined_data 

def cap_outliers(data, attribute, low=10, high=90):
    combined_data = pd.DataFrame()
    unique_countries = data.location.unique()
    for country in unique_countries:
        data_country = data[data.location == country]
        if data_country[attribute].values[0] != 0:
            lower_percentile = np.percentile(data_country[attribute], low)
            upper_percentile = np.percentile(data_country[attribute], high)
            data_capped = np.where(data_country[attribute] < lower_percentile, lower_percentile, data_country[attribute])
            data_capped = np.where(data_capped > upper_percentile, upper_percentile, data_capped)
            data_country[attribute] = data_capped
        combined_data = pd.concat([combined_data, data_country])
    return combined_data 




