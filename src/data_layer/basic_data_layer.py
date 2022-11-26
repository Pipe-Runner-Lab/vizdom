from connection.db_connector import DBConnection
from functools import lru_cache, cache
import pandas as pd
from .util import resample_by_date_range, resample_by, date_range, query_creator


def get_aggregated_total_cases_by_country(start_date=None, end_date=None, iso_code=None):
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df('iso_code, total_cases', 'covid', query)
    df = df.groupby(['iso_code']).sum().reset_index()
    return df


def get_attribute(attribute, start_date=None, end_date=None, iso_code=None, aggregation_type=None):
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df(f'date, location, {attribute}', 'covid', query)

    # When aggregation is done, we don't need to resample since date will have no meaning
    if aggregation_type == "mean":
        df = df.groupby(['location']).mean().reset_index()
        return df
    return resample_by_date_range(df, start_date, end_date)

def get_total_number_of_cases_by_date(iso_code=None, start_date=None, end_date=None):
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df('date, total_cases, location', 'covid', query)
    return resample_by_date_range(df, start_date, end_date)

@cache
def get_list_of_countries():
    df = DBConnection().get_df('iso_code, location', 'covid')
    df = df.groupby(['location', 'iso_code']).size().reset_index()
    dict = {}
    for iso_code, location in zip(df.iso_code, df.location):
        dict[iso_code] = {"label": location}
    return dict

