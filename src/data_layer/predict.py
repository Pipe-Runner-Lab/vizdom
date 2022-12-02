from sklearn.linear_model import LassoCV, Lasso, Ridge, ElasticNet
from crawlers.url_crawlers import get_our_world_in_data_attributes
import pandas as pd
from connection.db_connector import DBConnection
from .util import query_creator
from functools import lru_cache
from utils.util import hashable_cache, data_bars_diverging

all_attributes = list(get_our_world_in_data_attributes.keys())
all_attributes.remove('continent')
all_attributes.remove('iso_code')
all_attributes.remove('location')
all_attributes.remove('date')

@hashable_cache(lru_cache(maxsize=32))
def get_prediction(model_type, target_attribute, iso_code, attribute):
    attribute = all_attributes if attribute == None else attribute

    query = query_creator(iso_code=iso_code)
    data = DBConnection().get_df(f'date, location, {(", ").join(attribute)}', 'covid', query)
    data.set_index('date', inplace=True)
    data.index = pd.to_datetime(data.index, errors='coerce')
    x = pd.DataFrame(data[attribute])
    y = pd.DataFrame(data[target_attribute])

    x_sort = x.sort_index()
    y_sort = y.sort_index()

    # move data back by 3 months
    y_shift = y_sort.shift(-90)
    number_of_nans = y_shift.isnull().values.ravel().sum()
    y_shift_dropped = y_shift.dropna(axis=0)
    x_sort_dropped = x_sort.drop(x_sort.tail(number_of_nans).index)

    if model_type == "lasso":
        model = Lasso(alpha=0.01)
        model.fit(x_sort_dropped, y_shift_dropped[target_attribute])
    elif model_type == "ridge":
        model = Ridge(alpha=0.01)
        model.fit(x_sort_dropped, y_shift_dropped[target_attribute])
    else:
        raise ValueError("Model type not supported")

    y_hat = model.predict(x_sort)
    
    # move date forward by 3 months for plotting
    y_shift = y_shift.shift(90, freq='D')

    return y_hat, y_shift
