from dateutil import parser
import numpy as np
"""_summary_
Utility 

"""
def resample_by_date_range(df, range):
    max_points = map_value(range, 1, 1051, 236617, 2000)
    indices = np.round(np.linspace(0, df.shape[0] - 1, int(max_points/4))).astype(int)
    return df.iloc[indices]

def resample_by(df, denominator):
    max_points = int(df.shape[0]/denominator)
    indices = np.round(np.linspace(0, df.shape[0] - 1, max_points)).astype(int)
    return df.iloc[indices]

def date_range(start_date, end_date):
    if start_date != None and end_date != None:
        start_date = parser.parse(str(start_date)).date()
        end_date = parser.parse(str(end_date)).date()
        return abs(start_date-end_date).days
    return 1051


def map_value(in_v, in_min, in_max, out_min, out_max):           # (3)
    """Helper method to map an input value (v_in)
       between alternative max/min ranges."""
    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return v

def query_creator(iso_code=None, start_date=None, end_date=None):
    query = []
    
    if iso_code:
        query.append(f'iso_code = "{iso_code}"')
        
    if start_date and end_date:
        query.append(f'date BETWEEN "{start_date}" AND "{end_date}"')
        
    if len(query) != 0:
        return " AND ".join(query)
    else:
        return None
    