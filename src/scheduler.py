import schedule
from time import sleep
from pipeline import run_pipeline

# run_pipeline()
schedule.every().day.at('00:00').do(run_pipeline)

while True:
    schedule.run_pending()
    sleep(1)