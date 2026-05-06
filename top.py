"""
Python script voor schrijven naar parquet
"""

from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///d:/data/w/weer.db")

w = z = datetime.now() - timedelta(days=1)

w = int(w.strftime("%Y%m%d") + "00")
z = int(z.strftime("%Y%m%d") + "99")

query = f"SELECT * FROM fc WHERE r BETWEEN {w} AND {z}"

df = pd.read_sql(query, con=engine)

w = str(w)[:8]
df = df.astype("Int64")

df.to_parquet(
    f"d:/data/v/p/fc_{w}.parquet",
    engine="pyarrow",
    compression="zstd",
    index=False,
)
