from dateutil import parser
import numpy as np
import pandas as pd
"""_summary_
Utility 

"""
def resample_by_date_range(df, start_date, end_date):
    range = date_range(start_date, end_date)  
    max_points = map_value(range, 1, 1061, 219559, 1000)
    return resampled_by_country(df, max_points)

def resampled_by_country(df, max_points):
    unique_countries = df.location.unique()
    max_points = max_points/len(unique_countries)
    resampled = []
    for country in unique_countries:
        data = df[df.location == country]
        indices = np.round(np.linspace(0, data.shape[0] - 1, int(max_points))).astype(int)
        data.iloc[indices]
        resampled.append(data)
    return pd.concat(resampled)

def resample_by(df, denominator):
    max_points = int(df.shape[0]/denominator)
    return resampled_by_country(df, max_points)

def date_range(start_date, end_date):
    if start_date != None and end_date != None:
        start_date = parser.parse(str(start_date)).date()
        end_date = parser.parse(str(end_date)).date()
        return abs(start_date-end_date).days
    return 1061


def map_value(in_v, in_min, in_max, out_min, out_max):           # (3)
    """Helper method to map an input value (v_in)
       between alternative max/min ranges."""
    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return v

def query_creator(iso_code=None, start_date=None, end_date=None):
    query = []
    
    if iso_code:
        if isinstance(iso_code, list) and len(iso_code) == 1:
            iso_code = iso_code[0]
        
        if isinstance(iso_code, list):
            query.append(f"iso_code IN {tuple(iso_code)}")
        else:
            query.append(f'iso_code = "{iso_code}"')
        
    if start_date and end_date:
        query.append(f'date BETWEEN "{start_date}" AND "{end_date}"')
        
    if len(query) != 0:
        return " AND ".join(query)
    else:
        return None
    
    
