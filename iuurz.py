import requests
import zipfile
import io, sys
import pandas as pd
import sqlite3

url = "https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/uurgegevens/uurgeg_239_2021-2030.zip"
response = requests.get(url)

if response.status_code != 200:
    sys.exit()

with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    df = pd.read_csv(
        z.open("uurgeg_239_2021-2030.txt"), skiprows=24, skipinitialspace=True
    )

df.columns = df.columns.str.lower()
df.rename(
    columns={
        "# stn": "stn",
        "yyyymmdd": "d",
    },
    inplace=True,
)
df.drop("tz", axis=1, inplace=True)
df = df.round(0).astype("Int64")
print(df.columns)
conn = sqlite3.connect("d:/data/w/weer.db")

sql = "SELECT COALESCE(MAX(d), 0) FROM dh WHERE stn=239"
max_val = pd.read_sql_query(sql, conn).iloc[0, 0]

df = df[df["d"] > max_val]
print(max_val)

if not df.empty:
    df.to_sql("dh", conn, if_exists="append", index=False)


sql = """
INSERT OR IGNORE INTO 
meting (d, hh, mm,stn,dd,ff,fx,p,t,t10,vv,u,rh,s)
SELECT d, hh+2, 0,stn,dd,ff,fx,p,t,t10n,vv,u,rh,q 
FROM dh where hh < 22;
INSERT OR IGNORE INTO 
meting (d, hh, mm,stn,dd,ff,fx,p,t,t10,vv,u,rh,s)
SELECT 
CAST(strftime('%Y%m%d', date(substr(CAST(d AS TEXT), 1, 4) || '-' || 
substr(CAST(d AS TEXT), 5, 2) || '-' || 
substr(CAST(d AS TEXT), 7, 2), '+1 day')) AS INTEGER), 
hh-22, 0,stn,dd,ff,fx,p,t,t10n,vv,u,rh,q 
FROM dh where hh > 21;
update meting set ts=d*10000+hh*100+mm where ts is null;
"""
cursor = conn.cursor()

cursor.executescript(sql)

conn.commit()
conn.close()
