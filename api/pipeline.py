"""
We will use this file to define the pipeline for our cron job.
Pipeline if run using cron on a daily basis and will update the DB with the latest data.
The pipeline is as follows:
1. Get data using crawlers
2. Clean and filter the data using filters
3. Process data using the data engines
4. Store the data in the DB using the DB connection
"""

from db.connection import DBConnection

cur = DBConnection().get_cursor()
cur.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
cur.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
cur.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")

rows = cur.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)