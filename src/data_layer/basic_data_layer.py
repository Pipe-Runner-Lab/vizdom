from connection.db_connector import DBConnection
import pandas as pd
from .util import resample_by_date_range, resample_by, date_range, query_creator


def get_aggregated_total_cases_by_country(start_date=None, end_date=None, iso_code=None):
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df('iso_code, total_cases', 'covid', query)
    df = df.groupby(['iso_code']).sum().reset_index()
    return df


def get_attribute_by_date_range(attribute, start_date=None, end_date=None, iso_code=None):
    range = date_range(start_date, end_date)
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df(f'date, {attribute}', 'covid', query)
    return resample_by_date_range(df, range)

def get_attribute(attribute, start_date=None, end_date=None, iso_code=None):
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    return DBConnection().get_df(f'date, {attribute}', 'covid', query)

def get_total_number_of_cases_by_date(iso_code=None, start_date=None, end_date=None):
    range = date_range(start_date, end_date)
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df('date, total_cases', 'covid', query)
    return resample_by_date_range(df, range)


def get_list_of_countries():
    df = DBConnection().get_df('iso_code, location', 'covid')
    df = df.groupby(['location', 'iso_code']).size().reset_index()
    dict = {}
    for iso_code, location in zip(df.iso_code, df.location):
        dict[iso_code] = {"label": location}
    for country in dict:
        print(print(dict.get(country, {}).get('label')))
    return dict

