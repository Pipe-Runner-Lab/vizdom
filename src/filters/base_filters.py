"""
Filters are responsible for dropping unnecessary columns and filling NaNs.
"""
import pandas as pd
pd.options.mode.chained_assignment = None  # type: ignore # default='warn'

def drop_rows_with_OWID(data):
    data['is_continent'] = data['iso_code'].str.startswith('OWID')
    data = data[data['is_continent'] == False]
    del data['is_continent']
    return data
        
def drop_rows_with_occurrence_number(data, number):
    is_multi = data['location'].value_counts() > 1
    filtered = data[data['location'].isin(is_multi[is_multi].index)]
    return filtered
    

def remove_columns_or_rows_with_nan(data, axis, how):
    """Removes NaNs from the given axis and returns the data as a dataframe.
    param data: A dataframe containing the NaNs to remove.
    param axis: The axis to remove the NaNs from. Optional, default 0. 
    0 removes rows that contains NaNs.
    1 removes columns that contain NaNs.
    param how: Optional, default 'any' Specifies whether to remove NaNs all or any.  
    returns : DataFrame containing the NaNs removed. 
    """
    return data.dropna(axis=axis, how=how)


def keep_columns_by_name(data, columns):
    """
    Drops all the columns which is not the same as the given names from the list, and keeps the rest of the columns
    and returns the resulting data as DataFrame.

    ----------
    data : DataFrame
        The data you want to drop the columns
    columns : list
        The names of the columns you want to drop
    returns : DataFrame
        The data with the resulting columns
    """
    return data[columns]


def country_based_interpolation(df):
    output = pd.DataFrame()

    unique_countries = df.iso_code.unique()
    for country in unique_countries:
        data = df[df.iso_code == country]
        # sending a slice of the data [a copy]
        interpolated_date = fill_nans_by_interpolation(data)
        output = pd.concat([output, interpolated_date])

    return output

# TODO: This should ideally check if the column is numeric and then fill the NaNs
def fill_nans_by_interpolation(data):
    """_summary_
    Interpolation of the given data with the given attributes.
    Args:
        data (Dataframe): data to interpolate
        attributes (list): attributes for interpolating

    Returns:
        _type_: _description_
    """
    # Sort by date and then set date as index; needed for interpolation
    data = data.sort_values(by=["date"]).set_index("date")
    attributes = list(data.describe().columns)
    country = data.location.unique()
    iso_code = data.iso_code.unique()
    continent = data.continent.unique()
    for attr in attributes:
        column_data = data[attr]
        if column_data.isnull().all():
            column_data.iloc[::] = 0
        else:
            if pd.isna(column_data.iloc[0]):
                column_data.iloc[0] = column_data.loc[column_data.first_valid_index()]
            if pd.isna(column_data.iloc[-1]):
                column_data.iloc[-1] = column_data.loc[column_data.last_valid_index()]
         
        column_data_resampled = column_data.resample(
            "1d").asfreq()
        data_resampled = data.resample(
            "1d").asfreq()  # Resample to daily
        column_data_interpolated = column_data_resampled.interpolate(
            method='linear', order=1)  # Interpolation of the data
        data_resampled[['continent']] = data_resampled[['continent']].fillna(f'{continent[0]}')
        data_resampled[['iso_code']] = data_resampled[['iso_code']].fillna(f'{iso_code[0]}')
        data_resampled[['location']] = data_resampled[['location']].fillna(f'{country[0]}')
        # save to overwrite the original data
        data_resampled[attr] = column_data_interpolated
        data = data_resampled
    return data.reset_index()
