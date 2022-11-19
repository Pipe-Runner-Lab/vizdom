"""
Filters are responsible for dropping unnecessary columns and filling NaNs.
"""
import pandas as pd

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


def fill_nans_by_interpolation(data):
    """_summary_
    Interpolation of the given data with the given attributes.
    Args:
        data (Dataframe): data to interpolate
        attributes (list): attributes for interpolating

    Returns:
        _type_: _description_
    """
    attributes = list(data.describe().columns)
    for attr in attributes:
        s = data[attr].copy()
        if s.isnull().all():
            s[::] = 0
        else:
            if pd.isna(s[0]):
                s[0] = s.loc[s.first_valid_index()]
            if pd.isna(s[-1]):
                s[-1] = s.loc[s.last_valid_index()]
            
        data_resampled = s.resample("1d").asfreq() # Resample to daily
        data_resampled = data_resampled.interpolate(method='linear', order=1) # Interpolation of the data
        data[attr] = data_resampled
    return data