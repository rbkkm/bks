import pandas as pd
import glob
import os

tl = ["tg", "tn", "tx"]  # , "rr", "pp", "hu", "qq", "fg"]
tl = ["fg"]

for t in tl:

    bestanden = glob.glob(f"d:/eos/{t}_*.csv")

    for bestandsnaam in bestanden:
        # 2. Laad het bestand
        df = pd.read_csv(bestandsnaam, on_bad_lines="skip")

        # 3. Verwijder de streepjes uit de 'time' kolom
        # df["time"] = df["time"].astype(str).str.replace("-", "")
        # df["latitude"] = (df["latitude"] * 1e7).astype(int)
        # df["longitude"] = (df["longitude"] * 1e7).astype(int)
        df["latitude"] = (df["latitude"] // 1000 * 1000).astype(int)
        df["longitude"] = (df["longitude"] // 1000 * 1000).astype(int)

        # t_numeric = pd.to_numeric(df[t], errors="coerce")
        # df[t] = (t_numeric.round(1) * 10).fillna(0).astype(int)

        b = "d:/eos/c/" + os.path.basename(bestandsnaam)

        print(b)
        df.to_csv(b, index=False)
        print(f"verwerkt: {bestandsnaam}")

print("\nKlaar! Alle bestanden zijn verwerkt.")
