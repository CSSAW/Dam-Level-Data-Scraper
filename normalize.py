import pandas as pd
import os

def normalize_df(df):
    n_df = df.copy()

    n_df.rename({"This week": "This_Week", "Last Week": "Last_Week", "Last Year": "Last_Year"}, axis=1, inplace=True)

    # this columns are all percentages
    n_df["This_Week"] /= 100.0
    n_df["Last_Week"] /= 100.0
    n_df["Last_Year"] /= 100.0

    fsc_max = n_df["FSC"].max()
    fsc_min = n_df["FSC"].min()

    # squish the full storage capacity values between 0.1 and 0.9
    n_df["FSC"] = 0.1 + (n_df["FSC"] - fsc_min) * 0.8 / (fsc_max - fsc_min)

    return n_df

def get_norm_csv(path):
    old_csv = os.path.abspath(path)
    new_csv = os.path.join(os.path.dirname(old_csv), "norm_" + os.path.basename(old_csv))

    n_df = normalize_df(pd.read_csv(old_csv, sep=','))

    n_df.to_csv(new_csv, sep=',', index=False)
