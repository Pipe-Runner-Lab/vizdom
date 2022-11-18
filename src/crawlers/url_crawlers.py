import pandas as pd

def get_our_world_in_data():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    df = pd.read_csv(url)
    return df