import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description="Combine multiple CSVs into one")
parser.add_argument("path", help="The directory of CSVs")
args = parser.parse_args()

df = pd.DataFrame()
frames = []

for csv in os.scandir(args.path):
    if(csv.path.endswith(".csv") and csv.is_file()):
        frames.append(pd.read_csv(csv, sep=','))

df = df.append(frames)
df.sort_values(by=["Date"], inplace=True)
df.to_csv(os.path.join(args.path, "all_dam_levels.csv"), sep=',', index=False)
