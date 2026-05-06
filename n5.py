import xarray as xr
from pathlib import Path

t = "fg"

map = Path("d:/data/eos")
f = map / f"{t}_ens_mean_0.25deg_reg_pre1950.nc"

ds = xr.open_dataset(f)


for jaar in range(1800, 1951):

    try:
        print(f"Bezig met jaar: {jaar}...")

        ds_jaar = ds.sel(time=str(jaar))

    except Exception:
        # Vangt letterlijk elke fout op en gaat naar het volgende item
        print(jaar)
        continue

    df = ds_jaar.to_dataframe().dropna(subset=[t])

    bestandsnaam = map / f"{t}_{jaar}_50.csv"
    df.to_csv(bestandsnaam)
