from datetime import datetime
import pandas as pd


def get_our_world_in_data():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    df = pd.read_csv(url, parse_dates=['date'])
    return df


get_our_world_in_data_attributes = {
    'iso_code': {"type": 'TEXT', "label": 'ISO Code'},
    'continent': {"type": 'TEXT', "label": 'Continent'},
    'location': {"type": "TEXT", "label": "Location"},
    'date': {"type": "TEXT", "label": "Date"},
    'new_cases': {"type": "REAL", "label": "New Cases"},
    'total_cases': {"type": "REAL", "label": "Total Cases"},
    'new_deaths': {"type": "REAL", "label": "New Deaths"},
    'total_deaths': {"type": "REAL", "label": "Total Deaths"},
    'new_vaccinations': {"type": "REAL", "label": "New Vaccinations"},
    'total_vaccinations': {"type": "REAL", "label": "Total Vaccinations"},
    'people_vaccinated': {"type": "REAL", "label": "People Vaccinated"},
    'people_fully_vaccinated': {"type": "REAL", "label": "People Fully Vaccinated"},
    'female_smokers': {"type": "REAL", "label": "Female Smokers"},
    'male_smokers': {"type": "REAL", "label": "Male Smokers"},
    'extreme_poverty': {"type": "REAL", "label": "Extreme Poverty"},
    'life_expectancy': {"type": "REAL", "label": "Life Expectancy"},
    'population_density': {"type": "REAL", "label": "Population Density"},
}

get_our_world_in_data_real_attributes = {}

for key, value in zip(get_our_world_in_data_attributes.keys(), get_our_world_in_data_attributes.values()):
   if value['type'] == "REAL":
       get_our_world_in_data_real_attributes[key] = value
