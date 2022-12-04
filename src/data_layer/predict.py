from sklearn.linear_model import Lasso, Ridge
import pandas as pd
from connection.db_connector import DBConnection
from .util import query_creator
from functools import lru_cache
from utils.util import hashable_cache
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from crawlers.url_crawlers import get_our_world_in_data_real_attributes

model_params = {
    "lasso": {
        "alpha": 0.1,
        "max_iter": 10000,
    }
}

list_of_real_attributes = get_our_world_in_data_real_attributes.items()
all_attributes = [attribute for attribute, _ in list_of_real_attributes]

@hashable_cache(lru_cache(maxsize=32))
def get_prediction(model_type, target_attribute, iso_code, attribute, predict_days=90, params=None):
    if (attribute == None or len(attribute) == 0):
        attribute = all_attributes 
    else:
        attribute.append(target_attribute)
        attribute = list(set(attribute))

    query = query_creator(iso_code=iso_code)
    data = DBConnection().get_df(
        f'date, location, {(", ").join(attribute)}', 'covid', query)  # type: ignore
    data.set_index('date', inplace=True)
    data.index = pd.to_datetime(data.index, errors='coerce')
    x = pd.DataFrame(data[attribute])
    y = pd.DataFrame(data[target_attribute])

    x_sort = x.sort_index()
    y_sort = y.sort_index()

    # move data back by 3 months
    y_shift = y_sort.shift(-predict_days)
    number_of_nans = y_shift.isnull().values.ravel().sum()
    y_shift_dropped = y_shift.dropna(axis=0)
    x_sort_dropped = x_sort.drop(x_sort.tail(number_of_nans).index)
    
    
    if model_type == "lasso":
        alpha = model_params["lasso"]["alpha"]
        max_iter = model_params["lasso"]["max_iter"]
        if params:
            alpha = params.get("alpha", alpha)
            max_iter = params.get("max_iter", max_iter)
        steps_lasso = [
            ('scalar', StandardScaler()),
            ('poly', PolynomialFeatures(degree=2)),
            ('model', Lasso(alpha=float(alpha), fit_intercept=True, max_iter=int(max_iter)))
        ]
        model = Pipeline(steps_lasso)
        model.fit(x_sort_dropped, y_shift_dropped[target_attribute])
    elif model_type == "ridge":
        steps_ridge = [
            ('scalar', StandardScaler()),
            ('poly', PolynomialFeatures(degree=1)),
            ('model', Ridge(alpha=0.01, fit_intercept=True))
        ]
        model = Pipeline(steps_ridge)
        model.fit(x_sort_dropped, y_shift_dropped[target_attribute])
    else:
        raise ValueError("Model type not supported")

    y_hat = model.predict(x_sort)

    # move date forward by 3 months for plotting
    y_shift = y_shift.shift(predict_days, freq='D')

    return abs(y_hat), y_shift
