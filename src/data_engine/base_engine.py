"""
Engine will process data and add additional columns
"""
def compute_mean(data):
    attributes = list(data.describe().columns)
    for attr in attributes:
        mean = data[attr].mean()
        data.insert(len(data.columns), f'{attr} mean', mean, allow_duplicates=False) 
    return data 

def compute_std(data):
    attributes = list(data.describe().columns)
    for attr in attributes:
        mean = data[attr].std()
        data.insert(len(data.columns), f'{attr} mean', mean, allow_duplicates=False) 
    return data 

def compute_rolling_mean(data, window):
    attributes = list(data.describe().columns)
    for attr in attributes:
        rolling_mean = data[attr].rolling(window).mean()
        data[f'{attr} rolling mean'] = rolling_mean
    return data 

def compute_rolling_std(data, window):
    attributes = list(data.describe().columns)
    for attr in attributes:
        rolling_std = data[attr].rolling(window).std()
        data[f'{attr} rolling mean'] = rolling_std
    return data 

