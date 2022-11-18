"""
Filters are responsible for dropping unnecessary columns and filling NaNs.
"""


def fill_nans(df):
    df = df[["iso_code", "date", "new_cases", "total_cases"]]
    df['new_cases'].fillna((df['new_cases'].mean()), inplace=True)
    df['total_cases'].fillna((df['total_cases'].mean()), inplace=True)
    return df