import pandas as pd

# 1. Inlezen
df = pd.read_csv("d:/data/v/sv.csv", skipinitialspace=True)

# 2. E7 Berekening (direct nieuwe kolommen maken)
df["lat"] = (df["lat"] * 1e7).astype(int)
df["lon"] = (df["lon"] * 1e7).astype(int)

# 4. Schrijven naar CSV
df.to_csv("d:/data/v/sv_e7.csv", index=False)

# Check het resultaat
print(df.head())
