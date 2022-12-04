import pandas as pd
"""
Engine will process data and add additional columns
"""
def compute_mean(data):
    attributes = list(data.describe().columns)
    for attr in attributes:
        mean = data[attr].mean()
        data.insert(len(data.columns), f'{attr} mean', mean, allow_duplicates=False) 
    return data 

def compute_std(data):
    attributes = list(data.describe().columns)
    for attr in attributes:
        mean = data[attr].std()
        data.insert(len(data.columns), f'{attr} mean', mean, allow_duplicates=False) 
    return data 

def compute_rolling_mean(data, window):
    attributes = list(data.describe().columns)
    for attr in attributes:
        rolling_mean = data[attr].rolling(window).mean()
        data[f'{attr} rolling mean'] = rolling_mean
    return data 

def compute_rolling_std(data, window):
    attributes = list(data.describe().columns)
    for attr in attributes:
        rolling_std = data[attr].rolling(window).std()
        data[f'{attr} rolling mean'] = rolling_std
    return data 


def combine_data_with_mask(data_1, data_2):
    combined_data = pd.DataFrame()
    unique_countries = data_1.location.unique()
    data_1 = data_1.sort_values(by=["date"]).set_index("date")
    data_2 = data_2.sort_values(by=["date"]).set_index("date")  

    for country in unique_countries:
        data_covid = data_1[data_1.location == country]
        data_mask = data_2[data_2.location_name == country]
        
        if data_mask.index.min() != pd.NaT and (data_covid.index.min() < data_mask.index.min()):
            country = data_mask.location_name.unique()
            iso_code = data_mask.CountryCode.unique()
            location_id = data_mask.location_id.unique()
            date_range = pd.date_range(data_covid.index.min(), data_mask.index.max())
            data_mask = data_mask.resample('D').asfreq().reindex(date_range)
            data_mask[['location_id']] = data_mask[['location_id']].fillna(f'{location_id[0]}')
            data_mask[['CountryCode']] = data_mask[['CountryCode']].fillna(f'{iso_code[0]}')
            data_mask[['location_name']] = data_mask[['location_name']].fillna(f'{country[0]}')
            data_mask = data_mask.fillna(0)

        data_mask = data_mask.groupby(data_mask.index).first()  
        data_covid['mask_use_obs'] = data_mask['mask_use_obs']
        data_covid['mask_use_mean'] = data_mask['mask_use_mean']
        data_covid = data_covid.fillna(0)
        combined_data = pd.concat([combined_data, data_covid])
    return combined_data.reset_index()


