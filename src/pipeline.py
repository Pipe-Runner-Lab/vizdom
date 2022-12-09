"""
We will use this file to define the pipeline for our cron job.
Pipeline if run using cron on a daily basis and will update the DB with the latest data.
The pipeline is as follows:
1. Get data using crawlers
2. Clean and filter the data using filters
3. Process data using the data engines
4. Store the data in the DB using the DB connection
"""

from connection.db_connector import DBConnection
from crawlers.url_crawlers import get_mask_data, get_our_world_in_data, get_school_data, get_our_world_in_data_attributes
from filters.base_filters import country_based_interpolation, keep_columns_by_name, drop_rows_with_OWID, drop_rows_with_occurrence_number
from data_engine.base_engine import combine_data_with_mask, combine_data_with_school, cap_outliers

db = DBConnection()

def run_pipeline():
    print("Running pipeline...")
    attributes = get_our_world_in_data_attributes.keys()
    covid_general = get_our_world_in_data()
    covid_mask = get_mask_data()
    school_years = get_school_data()
    covid_general_filtered_data = drop_rows_with_OWID(covid_general)
    covid_general_filtered_data = drop_rows_with_occurrence_number(covid_general_filtered_data, 1)
    covid_general_interp_data = country_based_interpolation(covid_general_filtered_data)
    combined_data = combine_data_with_mask(covid_general_interp_data, covid_mask, 'mask_use_mean')
    combined_data = combine_data_with_school(combined_data, school_years)
    data = keep_columns_by_name(combined_data, attributes)
    # data = cap_outliers(data, 'mask_use_mean', 25, 75)
    latest_db_entry = db.get_df("date", "covid", "date=(SELECT MAX(date) FROM covid)") # get the latest entry from the database
    if latest_db_entry.empty:
        db.populate_with_data_frame('covid', data)
    else:
        rest_data = data[~(data['date'] <= latest_db_entry['date'][0])] # remove rows of data that is <= latest entry 
        db.populate_with_data_frame('covid', rest_data)


run_pipeline()