import pandas as pd
import glob
import os


tl = ["sd"]

for t in tl:

    bestanden = glob.glob(f"d:/data/ecab/sd/{t}_*.txt")

    for bestandsnaam in bestanden:
        # 2. Laad het bestand
        df = pd.read_csv(bestandsnaam, on_bad_lines="skip", skiprows=21)
        print(df.columns.tolist())

        # 3. Verwijder de streepjes uit de 'time' kolom
        # df["time"] = df["time"].astype(str).str.replace("-", "", regex=False)
        # df["latitude"] = (df["latitude"] * 1e7).astype(int)
        # df["longitude"] = (df["longitude"] * 1e7).astype(int)
        # df["latitude"] = (df["latitude"] // 1000 * 1000).astype(int)
        # df["longitude"] = (df["longitude"] // 1000 * 1000).astype(int)

        # t_numeric = pd.to_numeric(df[t], errors="coerce")
        # df[t] = (t_numeric.round(1) * 10).fillna(0).astype(int)

        b = "d:/data/ecab/sd/c/" + os.path.basename(bestandsnaam)

        print(b)
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df_f = df[df["Q_SD"] != 9]

        df_f.to_csv(b, index=False)
        print(f"verwerkt: {bestandsnaam}")

print("\nKlaar! Alle bestanden zijn verwerkt.")
