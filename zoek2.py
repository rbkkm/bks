import pandas as pd
from pathlib import Path
import csv

map = Path("d:/data/")
j = map / f"latlon.csv"

df = pd.read_csv("stations.csv", sep=",", skipinitialspace=True)
df.columns = [c.strip() for c in df.columns]
rt = "lat,lon,stn,name,country"
with open(j, mode="r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        target_lat, target_lon = float(row["lat"]), float(row["lon"])

        # Bereken de afstand (simpele Pythagoras voor kleine afstanden)
        df["afstand"] = (
            (df["LAT"] - target_lat) ** 2 + (df["LON"] - target_lon) ** 2
        ) ** 0.5
        dichtstbijzijnde = df.loc[df["afstand"].idxmin()]
        rt += (
            "\n"
            + str(target_lat)
            + ","
            + str(target_lon)
            + ","
            + str(dichtstbijzijnde["STN"])
            + ","
            + (dichtstbijzijnde["NAME"]).strip()
            + ","
            + (dichtstbijzijnde["CN"]).strip()
        )
        if 5 < target_lon < 6:
            print(f"Gevonden station: {dichtstbijzijnde['NAME']}")
        # print(f"Originele LAT in lijst: {dichtstbijzijnde['LAT']}")

with open(
    "stname.csv",
    "w",
    encoding="utf-8",
) as f_uit:
    f_uit.write(rt)
