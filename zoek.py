import pandas as pd
from pathlib import Path
import csv

map = Path("d:/data/")
j = map / f"latlon.csv"

df = pd.read_csv("stn.txt", sep="|", skipinitialspace=True)
df.columns = [c.strip() for c in df.columns]


target_lat, target_lon = 52.1, 5

print(target_lat, target_lon)

# Bereken de afstand (simpele Pythagoras voor kleine afstanden)
df["afstand"] = ((df["LAT"] - target_lat) ** 2 + (df["LON"] - target_lon) ** 2) ** 0.5
dichtstbijzijnde = df.loc[df["afstand"].idxmin()]

print(f"Gevonden station: {dichtstbijzijnde['NAME']}")
# print(f"Originele LAT in lijst: {dichtstbijzijnde['LAT']}")
