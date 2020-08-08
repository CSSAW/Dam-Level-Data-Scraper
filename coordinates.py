import pandas as pd
import os
import requests

def add_coords(df, key):
    n_df = df.copy()
    cache = {}

    lat = []
    lng = []

    for d in df["Dam"].values:
        if d not in cache:
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + d + "&region=za&key=" + key
            data = requests.get(url).json()

            if data["status"] == "OK":
                d_lat = data["results"][0]["geometry"]["location"]["lat"]
                d_lng = data["results"][0]["geometry"]["location"]["lng"]
                cache[d] = (d_lat, d_lng)
            else:
                print(data["status"] + " for " + d)
                cache[d] = (0, 0)

        pair = cache[d]
        lat.append(pair[0])
        lng.append(pair[1])

    n_df = n_df.assign(Latitude = lat)
    n_df = n_df.assign(Longitude = lng)

    return n_df
