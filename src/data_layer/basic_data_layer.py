from connection.db_connector import DBConnection

def get_aggregated_total_cases_by_country():
  df = DBConnection().get_df('iso_code, total_cases', 'covid')
  df = df.groupby(['iso_code']).sum().reset_index()
  return df