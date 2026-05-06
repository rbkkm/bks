import requests
import zipfile
import io, sys
import pandas as pd
import sqlite3

url = "https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/uurgegevens/jaar.zip"

response = requests.get(url)

if response.status_code != 200:
    sys.exit()

with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    df = pd.read_csv(z.open("jaar.txt"), skiprows=31, skipinitialspace=True)

df.columns = df.columns.str.lower()
df.rename(
    columns={
        "# stn": "stn",
        "yyyymmdd": "d",
    },
    inplace=True,
)
df = df.round(0).astype("Int64")
print(df.columns)
conn = sqlite3.connect("d:/data/w/weer.db")

sql = "SELECT COALESCE(MAX(d), 0) FROM dh"
max_val = pd.read_sql_query(sql, conn).iloc[0, 0]

df = df[df["d"] > max_val]

print(df)

if not df.empty:
    df.to_sql("dh", conn, if_exists="append", index=False)
