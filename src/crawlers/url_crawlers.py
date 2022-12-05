from datetime import datetime
import pandas as pd


def get_our_world_in_data():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    df = pd.read_csv(url, parse_dates=['date'])
    return df

def get_mask_data():
    url = '../data/covid_mask_data.csv'
    df = pd.read_csv(url, parse_dates=['date'])
    df = df.rename({'location_name': 'location', 'CountryCode': 'iso_code'}, axis=1)
    df = df.drop(columns=['location_id'])
    return df

def get_expected_years_of_school_data():
    url = '../data/covid_data.csv'
    df = pd.read_csv(url)
    df = df.rename({'country': 'location'}, axis=1)
    df = df.drop(columns=['income_group', 'Unnamed: 0', 'population', 'total_tests', 'total_cases', 'total_deaths', 'total_recovered'])
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
    'population': {"type": "REAL", "label": "Population"},
    'human_development_index': {"type": "REAL", "label": "Human Development Index"},
    'diabetes_prevalence': {"type": "REAL", "label": "Diabetes Prevalence"},
    'cardiovasc_death_rate': {"type": "REAL", "label": "Cardiovasc Death Rate"},
    'gdp_per_capita': {"type": "REAL", "label": "GDP per Capita"},
    'median_age': {"type": "REAL", "label": "Median Age"},
    'total_boosters': {"type": "REAL", "label": "Total Boosters"}, 
    'hosp_patients': {"type": "REAL", "label": "Hospital Patients"},
    'stringency_index': {"type": "REAL", "label": "Stringency Index"},
    'mask_use_mean': {"type": "REAL", "label": "Mask Use Mean"},
    'expected_years_of_school': {"type": "REAL", "label": "Expected Years of School"}
}

get_our_world_in_data_real_attributes = {}

for key, value in zip(get_our_world_in_data_attributes.keys(), get_our_world_in_data_attributes.values()):
   if value['type'] == "REAL":
       get_our_world_in_data_real_attributes[key] = value
