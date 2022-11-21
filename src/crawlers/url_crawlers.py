from datetime import datetime
import pandas as pd


def get_our_world_in_data():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    df = pd.read_csv(url, parse_dates=['date'])
    return df


get_our_world_in_data_attributes = {
    'iso_code': 'TEXT', 'date': "TEXT", 
    'new_cases': "REAL", 'total_cases': "REAL", 
    'new_deaths': "REAL", 'total_deaths': "REAL",
    'new_vaccinations': "REAL", 'total_vaccinations': "REAL",
    'people_vaccinated': "REAL", 'people_fully_vaccinated': "REAL",
    'female_smokers': "REAL", 'male_smokers': "REAL",
    'extreme_poverty': "REAL", 'life_expectancy': "REAL",
    'population_density': "REAL"
}
