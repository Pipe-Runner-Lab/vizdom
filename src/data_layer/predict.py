from sklearn.linear_model import Lasso, Ridge
import pandas as pd
from connection.db_connector import DBConnection
from .util import query_creator
from functools import lru_cache
from utils.util import hashable_cache
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from crawlers.url_crawlers import get_attributes_for_predict

model_params = {
    "lasso": {
        "alpha": 0.0001,
        "max_iter": 100000,
    },
    "ridge": {
        "alpha": 0.0001,
        "max_iter": 100000,
    }
}

list_of_predict_attributes = get_attributes_for_predict.items()
all_attributes = [attribute for attribute, _ in list_of_predict_attributes]

@hashable_cache(lru_cache(maxsize=32))
def get_prediction(model_types, target_attribute, iso_code, attribute, predict_days=90):
    if (attribute == None or len(attribute) == 0):
        attribute = all_attributes 
    else:
        attribute.append(target_attribute)
        attribute = list(set(attribute))

    query = query_creator(iso_code=iso_code)
    data = DBConnection().get_df(
        f'date, location, {(", ").join(attribute)}', 'covid', query)  
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
    
    y_hat = {}
    for model_type in model_types:
        alpha = model_params[model_type]["alpha"]
        max_iter = model_params[model_type]["max_iter"]
        if model_type == "lasso":
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
                ('poly', PolynomialFeatures(degree=2)),
                ('model', Ridge(alpha=float(alpha), fit_intercept=True, max_iter=int(max_iter)))
            ]
            model = Pipeline(steps_ridge)
            model.fit(x_sort_dropped, y_shift_dropped[target_attribute])
        else:
            raise ValueError("Model type not supported")

        y_hat[model_type] = abs(model.predict(x_sort))
        
    # move date forward by 3 months for plotting
    y_shift = y_shift.shift(predict_days, freq='D')

    return y_hat, y_shift
