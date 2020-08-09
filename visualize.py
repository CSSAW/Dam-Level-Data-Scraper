import plotly.express as px
import pandas as pd

def visualize_diff(df, date):
    n_df = df.loc[df["Date"] == date & df["Latitude"] != 0]
    n_df["diff"] = n_df["This_Week"] - n_df["Last_Week"]
 
    fig = px.scatter_mapbox(n_df, lat="Latitude", lon="Longitude", color="diff", size="FSC",
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=4, mapbox_style="carto-positron")
    fig.show()

def visualize_diff_timeline(df):
    n_df = df.loc[df["Latitude"] != 0]
    n_df["diff"] = n_df["This_Week"] - n_df["Last_Week"]

    fig = px.scatter_mapbox(n_df, lat="Latitude", lon="Longitude", color="diff", size="FSC", 
                  animation_frame="Date", color_continuous_scale=px.colors.cyclical.IceFire, 
                  zoom=4, mapbox_style="carto-positron")
    fig.show()
