from connection.db_connector import DBConnection
from dateutil import parser
import numpy as np


def get_aggregated_total_cases_by_country(iso_code=None):
    df = DBConnection().get_df('iso_code, total_cases', 'covid',
                               f'iso_code = "{iso_code}"' if iso_code else None)
    df = df.groupby(['iso_code']).sum().reset_index()
    return df

def get_total_number_of_cases_by_date(start_date=None, end_date=None):
    range = date_range(start_date, end_date)
    df = DBConnection().get_df('date, total_cases', 'covid', 
                               f'date BETWEEN "{start_date}" AND "{end_date}"' if start_date != None and end_date != None else None)
    
    max_points = map_value(range, 1, 1051, 236155, 2000)
    print(max_points, range)
    indices = np.round(np.linspace(0, df.shape[0] - 1, int(max_points))).astype(int)
    return df[indices]


def get_list_of_countries():
    df = DBConnection().get_df('iso_code', 'covid')
    return df['iso_code'].unique().tolist()

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