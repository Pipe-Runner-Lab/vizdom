from datetime import datetime
import pandas as pd


def get_our_world_in_data():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    df = pd.read_csv(url, parse_dates=['date'])
    return df


get_our_world_in_data_attributes = {
    'iso_code': 'TEXT', 'date': "TEXT", 'new_cases': "REAL", 'total_cases': "REAL"
}
