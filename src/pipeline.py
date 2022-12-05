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
from crawlers.url_crawlers import get_mask_data, get_our_world_in_data, get_expected_years_of_school_data, get_our_world_in_data_attributes
from filters.base_filters import country_based_interpolation, keep_columns_by_name, drop_rows_with_OWID, drop_rows_with_occurrence_number
from data_engine.base_engine import combine_data_with_mask, combine_data_with_expected_years_of_school, cap_outliers

db = DBConnection()
attributes = get_our_world_in_data_attributes.keys()
covid_general = get_our_world_in_data()
covid_mask = get_mask_data()
expected_years_of_school = get_expected_years_of_school_data()
filtered_data = drop_rows_with_OWID(covid_general)
filtered_data = drop_rows_with_occurrence_number(filtered_data, 1)
interpolated_data = country_based_interpolation(filtered_data)
combined_data = combine_data_with_mask(interpolated_data, covid_mask, 'mask_use_mean')
combined_data = combine_data_with_expected_years_of_school(combined_data, expected_years_of_school)
remaining_data = keep_columns_by_name(combined_data, attributes)
remaining_data = cap_outliers(remaining_data, 'mask_use_mean')
db.populate_with_data_frame('covid', remaining_data)