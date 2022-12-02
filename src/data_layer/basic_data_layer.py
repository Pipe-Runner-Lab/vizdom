from connection.db_connector import DBConnection
from functools import lru_cache, cache
import pandas as pd
from .util import resample_by_date_range, query_creator
from scipy.stats.stats import pearsonr
from utils.util import hashable_cache, data_bars_diverging
from crawlers.url_crawlers import get_our_world_in_data_attributes, get_our_world_in_data_real_attributes

@hashable_cache(lru_cache(maxsize=32))
def get_filtered_countries(iso_code, attribute_conditions):
    query = query_creator(iso_code=iso_code)
    attributes_to_check = [attribute for attribute,
                           condition in attribute_conditions]
    df = DBConnection().get_df(
        f'iso_code, {(", ").join(attributes_to_check)}', 'covid', query)
    df = df.groupby(['iso_code']).mean().reset_index()

    for filter in attribute_conditions:
        attribute = filter[0]
        conditions = filter[1]

        for condition in conditions:
            if condition['type'] == 'gt':
                df = df[df[attribute] > float(condition['value'])]
            elif condition['type'] == 'lt':
                df = df[df[attribute] < float(condition['value'])]
            elif condition['type'] == 'eq':
                df = df[df[attribute] == float(condition['value'])]
            elif condition['type'] == 'gte':
                df = df[df[attribute] >= float(condition['value'])]
            elif condition['type'] == 'lte':
                df = df[df[attribute] <= float(condition['value'])]
            elif condition['type'] == 'neq':
                df = df[df[attribute] != float(condition['value'])]

    return df["iso_code"].unique().tolist()


@hashable_cache(lru_cache(maxsize=32))
def get_aggregated_total_cases_by_country(start_date=None, end_date=None, iso_code=None):
    query = query_creator(
        iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df('iso_code, total_cases, location', 'covid', query)
    df = df.groupby(['iso_code', 'location']).sum().reset_index()
    return df


@hashable_cache(lru_cache(maxsize=32))
def get_attribute(attribute, start_date=None, end_date=None, iso_code=None, aggregation_type=None, resample=True):
    query = query_creator(
        iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df(f'date, location, {attribute}', 'covid', query)

    # When aggregation is done, we don't need to resample since date will have no meaning
    if aggregation_type == "mean":
        return get_aggregate(df, attribute, aggregation_type)
    elif aggregation_type == "sum":
        return get_aggregate(df, attribute, aggregation_type)
    elif aggregation_type == "latest":
        return get_latest(df, attribute)
    if resample:
        return resample_by_date_range(df, start_date, end_date)
    return df


@hashable_cache(lru_cache(maxsize=32))
def get_total_number_of_cases_by_date(iso_code=None, start_date=None, end_date=None):
    query = query_creator(
        iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df('date, total_cases, location', 'covid', query)
    return resample_by_date_range(df, start_date, end_date)


@cache
def get_list_of_countries():
    df = DBConnection().get_df('iso_code, location', 'covid')
    df = df.groupby(['location', 'iso_code']).size().reset_index()
    dict = {}
    for iso_code, location in zip(df.iso_code, df.location):
        dict[iso_code] = {"label": location}
    return dict


@hashable_cache(lru_cache(maxsize=32))
def compute_corr_two_attributes(attribute_1, attribute_2, start_date=None, end_date=None, iso_code=None):
    df1 = get_attribute(attribute_1, start_date, end_date, iso_code, None, False)
    df2 = get_attribute(attribute_2, start_date, end_date, iso_code, None, False)
    df1[attribute_2] = df2[attribute_2]
    unique_countries = df1.location.unique()
    corr_matrix = []
    for country in unique_countries:
        data = df1[df1.location == country]
        corr = pearsonr(data[attribute_1], data[attribute_2])
        corr_matrix.append([country, round(corr[0], 6)])
    data_corr = pd.DataFrame(corr_matrix, columns=[
        'Country', 'Correlation'])
    return data_corr.sort_values(by=['Correlation'], ascending=False)

@hashable_cache(lru_cache(maxsize=32))
def compute_corr_attributes(attribute, start_date=None, end_date=None, iso_code=None):
    df1 = get_attribute(attribute, start_date, end_date, iso_code, None, False)
    attributes = list(get_our_world_in_data_real_attributes.keys())
    for attr in attributes:
        if attr != attribute:
            attr_label = get_our_world_in_data_real_attributes[attr]["label"]
            df2 = get_attribute(attr, start_date, end_date, iso_code, None, False)
            df1[attr_label] = df2[attr]
    corr_matrix = df1.corr(method='pearson')[[attribute]]
    corr_matrix = corr_matrix.dropna()
    corr_matrix = corr_matrix.reset_index()
    corr_matrix.rename(columns={'index': 'Attributes', attribute: 'Correlation'}, inplace=True)
    corr_matrix = corr_matrix.sort_values(by=['Correlation'], ascending=False)
    corr_matrix = corr_matrix[corr_matrix['Attributes'] != attribute]
    corr_matrix['Correlation'] = corr_matrix['Correlation'].round(decimals = 6)
    return corr_matrix


def get_latest(df, attribute):
    latest_data = pd.DataFrame(columns=['location', attribute])
    unique_countries = df.location.unique()
    for country in unique_countries:
        data = df[df.location == country]
        del data['date']
        latest = data.tail(1)
        latest_data = pd.concat([latest_data, latest])
    return latest_data.reset_index()

def get_aggregate(df, attribute, type):
    agg_data = pd.DataFrame()
    values = []
    unique_countries = df.location.unique()
    agg_data['location'] = unique_countries
    for country in unique_countries:
        data = df[df.location == country]
        value = 0
        if type == 'mean':
            value = data[attribute].mean()
        elif type == 'sum':
            value = data[attribute].sum()
        values.append(value)
    agg_data[attribute] = values
    return agg_data

def create_table_bar_styles_multiple_countries(attribute_1, attribute_2, start_date, end_date, iso_code):
    correlation = compute_corr_two_attributes(
        attribute_1, attribute_2, start_date, end_date, iso_code)
    data = correlation.to_dict('records')
    columns = [{"name": i, "id": i} for i in correlation.columns]
    style = data_bars_diverging('Correlation')
    return data, columns, style

def create_table_bar_styles(attribute_1, start_date, end_date, iso_code):
    correlation = compute_corr_attributes(
        attribute_1, start_date, end_date, iso_code)
    data = correlation.to_dict('records')  # type: ignore
    columns = [{"name": i, "id": i} for i in correlation.columns]
    style = data_bars_diverging('Correlation')
    return data, columns, style
