import xarray as xr
from pathlib import Path

# tl = ["tg", "tn", "tx", "rr", "pp", "hu", "fg"]
tl = ["fg"]
for t in tl:

    map = Path("d:/data/eos")
    f = map / f"{t}_ens_spread_0.25deg_reg_v32.0e.nc"
    ds = xr.open_dataset(f)

    for jaar in range(1950, 2026):

        try:
            ds_jaar = ds.sel(time=str(jaar))

        except Exception:
            # Vangt letterlijk elke fout op en gaat naar het volgende item
            print(jaar)
            continue

        print(f"Bezig met jaar: {jaar}...")

        df = ds_jaar.to_dataframe().dropna(subset=[t])

        bestandsnaam = map / f"{t}_{jaar}_spread.csv"
        df.to_csv(bestandsnaam)
