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
from crawlers.url_crawlers import get_our_world_in_data
from filters.base_filters import fill_nans

db = DBConnection()

raw_data = get_our_world_in_data()
filtered_data = fill_nans(raw_data)
# skipping processing
db.populate_with_data_frame('covid', filtered_data)