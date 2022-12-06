from connection.db_connector import DBConnection
from functools import lru_cache, cache
import pandas as pd
from .util import resample_by_date_range, query_creator
from scipy.stats.stats import pearsonr
from utils.util import hashable_cache, data_bars_diverging
from crawlers.url_crawlers import get_our_world_in_data_real_attributes
from filters.filter_groups import custom_groups, quartiles


@hashable_cache(lru_cache(maxsize=32))
def get_filtered_countries(iso_code, attribute_conditions):
    query = query_creator(iso_code=iso_code)
    attributes_to_check = [attribute for attribute, condition in attribute_conditions]
    df = DBConnection().get_df(
        f'iso_code, {(", ").join(attributes_to_check)}', "covid", query
    )
    df = df.groupby(["iso_code"]).mean().reset_index()

    for filter in attribute_conditions:
        attribute = filter[0]
        conditions = filter[1]

        for condition in conditions:
            if condition["type"] == "gt":
                df = df[df[attribute] > float(condition["value"])]
            elif condition["type"] == "lt":
                df = df[df[attribute] < float(condition["value"])]
            elif condition["type"] == "eq":
                df = df[df[attribute] == float(condition["value"])]
            elif condition["type"] == "gte":
                df = df[df[attribute] >= float(condition["value"])]
            elif condition["type"] == "lte":
                df = df[df[attribute] <= float(condition["value"])]
            elif condition["type"] == "neq":
                df = df[df[attribute] != float(condition["value"])]

    return df["iso_code"].unique().tolist()


@hashable_cache(lru_cache(maxsize=32))
def get_simple_filtered_countries(
    continent=None, group=None, selected_group=None, should_group=False
):
    df = DBConnection().get_df("iso_code, gdp_per_capita, continent", "covid")

    if continent:
        df = df[df.continent.isin(continent)]

    countries = df.iso_code.unique().tolist()

    # if grouping is needed
    if selected_group and group:
        countries = []
        group_title = group
        group = {
            group_title: {},
        }

        if group_title in list(quartiles.keys()):
            column = quartiles[group_title]["column"]
            quantile = 1 / len(list(custom_groups[group_title].keys()))
            curr_quantile = quantile

            idx = 0
            for available_group in list(custom_groups[group_title].keys()):
                if idx == 0:
                    group[group_title][available_group] = (
                        df[df[column] < df[column].quantile(curr_quantile)]
                        .iso_code.unique()
                        .tolist()
                    )
                elif idx == len(selected_group) - 1:
                    group[group_title][available_group] = (
                        df[df[column] >= df[column].quantile(curr_quantile)]
                        .iso_code.unique()
                        .tolist()
                    )
                else:
                    group[group_title][available_group] = (
                        df[
                            (df[column] >= df[column].quantile(curr_quantile))
                            & (
                                df[column]
                                < df[column].quantile(curr_quantile + quantile)
                            )
                        ]
                        .iso_code.unique()
                        .tolist()
                    )
                curr_quantile += quantile

            temp_group = {
                group_title: {},
            }
            for picked_group in selected_group:
                temp_group[group_title][picked_group] = group[group_title][picked_group]
                countries += temp_group[group_title][picked_group]

            group = temp_group
        else:
            raise Exception("Not implemented")

        countries = list(set(countries))
    else:
        group = {
            "continent": {},
        }
        for continent in df.continent.unique():
            group["continent"][continent] = (
                df[df.continent == continent].iso_code.unique().tolist()
            )

    return countries, group if should_group else None


@hashable_cache(lru_cache(maxsize=32))
def get_aggregated_total_cases_by_country(
    attribute, start_date=None, end_date=None, iso_code=None, aggregation_type="latest"
):
    df = get_attribute(attribute, start_date, end_date, iso_code)
    return get_aggregate(df, attribute, aggregation_type)


@hashable_cache(lru_cache(maxsize=32))
def get_attribute(
    attribute,
    start_date=None,
    end_date=None,
    iso_code=None,
    aggregation_type=None,
    group=None,
):
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df(
        f"date, continent, location, iso_code, {attribute}", "covid", query
    )

    if group:
        return get_aggregate_grouped(df, attribute, aggregation_type, group)

    # When aggregation is done, we don't need to resample since date will have no meaning
    if aggregation_type != None and aggregation_type != "none":
        return get_aggregate(df, attribute, aggregation_type, None)

    return resample_by_date_range(df, start_date, end_date)


@hashable_cache(lru_cache(maxsize=32))
def get_total_number_of_cases_by_date(iso_code=None, start_date=None, end_date=None):
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df("date, total_cases, location", "covid", query)
    return resample_by_date_range(df, start_date, end_date)


@cache
def get_list_of_countries():
    df = DBConnection().get_df("iso_code, location", "covid")
    df = df.groupby(["location", "iso_code"]).size().reset_index()
    dict = {}
    for iso_code, location in zip(df.iso_code, df.location):
        dict[iso_code] = {"label": location}
    return dict


@cache
def get_list_of_continents():
    df = DBConnection().get_df("continent", "covid")
    df = df.groupby(["continent"]).size().reset_index()
    dict = {}
    for continent in df.continent:
        dict[continent] = {"label": continent}
    return dict


@hashable_cache(lru_cache(maxsize=32))
def compute_corr_two_attributes(
    attribute_1, attribute_2, start_date=None, end_date=None, iso_code=None
):
    attributes = [attribute_1, attribute_2]
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df(
        f'date, location, {(", ").join(attributes)}', "covid", query
    )
    unique_countries = df.location.unique()
    corr_matrix = []
    for country in unique_countries:
        data = df[df.location == country]
        corr = []
        if ((data[attribute_1] == data[attribute_1].iloc[0]).all()) or (
            (data[attribute_2] == data[attribute_2].iloc[0]).all()
        ):
            corr = [0, 0]
        else:
            corr = pearsonr(data[attribute_1], data[attribute_2])
        corr_matrix.append([country, round(corr[0], 6)])
    data_corr = pd.DataFrame(corr_matrix, columns=["Country", "Correlation"])
    return data_corr.sort_values(by=["Correlation"], ascending=False)


@hashable_cache(lru_cache(maxsize=32))
def compute_corr_attributes(attribute, start_date=None, end_date=None, iso_code=None):
    attributes = get_our_world_in_data_real_attributes.keys()
    query = query_creator(iso_code=iso_code, start_date=start_date, end_date=end_date)
    df = DBConnection().get_df(
        f'date, location, {(", ").join(attributes)}', "covid", query
    )

    corr_matrix = df.corr(method="pearson")[[attribute]]
    corr_matrix = corr_matrix.fillna(0)
    corr_matrix = corr_matrix.reset_index()
    corr_matrix.rename(
        columns={"index": "Attributes", attribute: "Correlation"}, inplace=True
    )
    # corr_matrix = corr_matrix.sort_values(by=['Correlation'], ascending=False)
    corr_matrix = corr_matrix[corr_matrix["Attributes"] != attribute]
    corr_matrix["Correlation"] = corr_matrix["Correlation"].round(decimals=6)
    return corr_matrix


def get_latest(df, attribute):
    latest_data = pd.DataFrame(columns=["location", attribute])
    unique_countries = df.location.unique()
    for country in unique_countries:
        data = df[df.location == country]
        del data["date"]
        latest = data.tail(1)
        latest_data = pd.concat([latest_data, latest])
    return latest_data.reset_index()


def get_aggregate(df, attribute, type, group_column=None):
    if type == "mean":
        return df.groupby(by=["location", "iso_code"], as_index=False)[attribute].mean()
    elif type == "sum":
        return df.groupby(["location", "iso_code"], as_index=False)[attribute].sum()
    elif type == "latest":
        return get_latest(df, attribute)
    raise Exception("Invalid aggregation type")


def get_aggregate_grouped(df, attribute, type, group_data):
    group_column = list(group_data.keys())[0]
    grouped_data = pd.DataFrame(columns=[group_column, attribute])
    
    for group, countries in group_data[group_column].items():
        df = df[df.iso_code.isin(countries)]
        if type == "mean":
            agg_value = df[attribute].mean()
        elif type == "sum":
            agg_value = df[attribute].sum()
        elif type == "latest":
            # TODO: Implement latest
            raise Exception("Invalid aggregation type")
        else:
            raise Exception("Invalid aggregation type")
        grouped_data = pd.concat(
            [grouped_data, pd.DataFrame({group_column: [group], attribute: [agg_value]})], ignore_index=True
        )
    return grouped_data


def create_table_bar_styles_multiple_countries(
    attribute_1, attribute_2, start_date, end_date, iso_code
):
    correlation = compute_corr_two_attributes(
        attribute_1, attribute_2, start_date, end_date, iso_code
    )
    data = correlation.to_dict("records")
    columns = [{"name": i, "id": i} for i in correlation.columns]
    style = data_bars_diverging("Correlation")
    return data, columns, style


def create_table_bar_styles(attribute_1, start_date, end_date, iso_code):
    correlation = compute_corr_attributes(attribute_1, start_date, end_date, iso_code)
    data = correlation.to_dict("records")
    modified_data = []
    for item in data:
        modified_data.append(
            {
                "Attributes": get_our_world_in_data_real_attributes[item["Attributes"]][
                    "label"
                ],
                "Correlation": item["Correlation"],
            }
        )
    columns = [{"name": i, "id": i} for i in correlation.columns]
    style = data_bars_diverging("Correlation")
    return modified_data, columns, style
