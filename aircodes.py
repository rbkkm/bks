import pandas as pd

# 1. Laad je bestand in
df = pd.read_csv("d:/data/a/airport-codes.csv")

# 2. Splitsen en omzetten naar getallen
df[["lat", "lon"]] = df["coordinates"].str.split(",", expand=True).apply(pd.to_numeric)


def transform_coords(df):
    # --- KOLOM 1: 3 decimalen * 10^7 ---
    df["lat_3dec_e7"] = (df["lat"].round(3) * 1e7).astype(int)
    df["lon_3dec_e7"] = (df["lon"].round(3) * 1e7).astype(int)

    # --- KOLOM 2: 3 decimalen -> naar kwart (0.250) -> * 10^7 ---
    # We gebruiken (waarde * 4) afronden op heel getal, en dan weer delen door 4
    # om exact op kwarten (0.0, 0.25, 0.5, 0.75) uit te komen.
    df["lat_qtr_e7"] = ((df["lat"].round(3) * 4).round() / 4 * 1e7).astype(int)
    df["lon_qtr_e7"] = ((df["lon"].round(3) * 4).round() / 4 * 1e7).astype(int)

    return df


# Toepassen
df = transform_coords(df)

# Kolom 'coordinates' wegdoen voor het overzicht
df = df.drop(columns=["coordinates"])

# Resultaat opslaan
df.to_csv("vliegvelden_geconverteerd.csv", index=False)

# Check het resultaat voor de eerste regel
print(df[["ident", "lat_3dec_e7", "lat_qtr_e7"]].head())
