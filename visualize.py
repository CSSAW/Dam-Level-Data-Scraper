import plotly.express as px
import pandas as pd

def visualize_diff(df, date):
    n_df = df.loc[df["Date"] == date]
    n_df["diff"] = n_df["This_Week"] - n_df["Last_Week"]

    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="diff", size="FSC",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                  mapbox_style="carto-positron")
    fig.show()
