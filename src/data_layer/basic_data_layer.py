from connection.db_connector import DBConnection
from .util import resample_by_date_range, date_range, query_creator


def get_aggregated_total_cases_by_country(iso_code=None):
    df = DBConnection().get_df('iso_code, total_cases', 'covid',
                               f'iso_code = "{iso_code}"' if iso_code else None)
    df = df.groupby(['iso_code']).sum().reset_index()
    return df


def get_attribute(attribute, start_date, end_date, iso_code=None):
    range = date_range(start_date, end_date)
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df(f'date, {attribute}', 'covid', query)
    return resample_by_date_range(df, range)

def get_total_number_of_cases_by_date(start_date=None, end_date=None):
    range = date_range(start_date, end_date)
    df = DBConnection().get_df('date, total_cases', 'covid',
                               f'date BETWEEN "{start_date}" AND "{end_date}"' if start_date and end_date else None)
    return resample_by_date_range(df, range)


def get_list_of_countries():
    df = DBConnection().get_df('iso_code', 'covid')
    return df['iso_code'].unique().tolist()
