import os
import requests
import sys
import pandas as pd
import io
import scraper_helpers
import argparse

parser = argparse.ArgumentParser(description="Scrape South African dam water level data from the Internet Archive")
parser.add_argument("--output", "-o", default="dam_data", help="directory where the CSVs will go")
parser.add_argument("--provinces", "-p", nargs='+', help="ids of the specific provinces to download")
parser.add_argument("--no_override", "-n", action='store_true', help="will not redownload data that is already present")
args = parser.parse_args()

if not os.path.exists(args.output): # create the output folder if it doesn't exist
    os.mkdir(args.output)

# hardcoding the provinces because those aren't changing anytime soon
provinces = {"EC":"Eastern_Cape",
            "FS":"Free_State",
            "G":"Gauteng",
            "KN":"KwaZulu_Natal",
            "LP":"Limpopo",
            "M":"Mpumalanga",
            "NC":"Northern_Cape",
            "NW":"North_West",
            "WC":"Western_Cape"}

# go through and check that the provinces we want exist in the dict and filter for the ones we want
if not args.provinces == None:
    new_provs = dict()
    for p in args.provinces:
        if p not in provinces:
            raise ValueError("invalid province id")
        else:
            new_provs[p] = provinces[p]

    provinces = new_provs

for p, name in provinces.items():
    csvPath = os.path.join(args.output, name + "_dam_levels.csv")
    if os.path.isfile(csvPath) and args.no_override:
        continue

    provinceData = list()

    for pair in scraper_helpers.getArchivedURLs(p):
        provinceData = provinceData + scraper_helpers.getTableData(pair[1], pair[0])

    df = pd.DataFrame(data=provinceData, columns=["Date", "Dam", "River", "FSC", "This week", "Last Week", "Last Year"])
    df.to_csv(csvPath, sep=",", index=False)

    print("Exported data to " + csvPath)
    