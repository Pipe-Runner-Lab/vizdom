from connection.db_connector import DBConnection


def get_aggregated_total_cases_by_country(iso_code=None):
    df = DBConnection().get_df('iso_code, total_cases', 'covid',
                               f'iso_code = "{iso_code}"' if iso_code else None)
    df = df.groupby(['iso_code']).sum().reset_index()
    return df

def get_total_number_of_cases_by_date(start_date=None, end_date=None):
    df = DBConnection().get_df('date, total_cases', 'covid')
    return df


def get_list_of_countries():
    df = DBConnection().get_df('iso_code', 'covid')
    return df['iso_code'].unique().tolist()
