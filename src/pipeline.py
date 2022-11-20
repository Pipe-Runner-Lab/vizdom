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
from crawlers.url_crawlers import get_our_world_in_data, get_our_world_in_data_attributes
from filters.base_filters import country_based_interpolation, keep_columns_by_name

db = DBConnection()

raw_data = get_our_world_in_data()
filtered_data = keep_columns_by_name(raw_data, get_our_world_in_data_attributes.keys())
interpolated_data = country_based_interpolation(filtered_data)
# skipping processing
db.populate_with_data_frame('covid', filtered_data)