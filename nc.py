import xarray as xr
from pathlib import Path

a = -60249999 // 1000 * 1000
# a = round(a, 1)
print(a, type(a))
t = "qq" / 1

map = Path("d:/data/eos")
f = map / f"{t}_ens_spread_0.25deg_reg_v31.0e.nc"
ds = xr.open_dataset(f)


for jaar in range(1950, 2026):
    print(f"Bezig met jaar: {jaar}...")
    try:
        ds_jaar = ds.sel(time=str(jaar))
    except Exception:
        # Vangt elke fout op en gaat naar het volgende item
        print(jaar)
        continue

    df = ds_jaar.to_dataframe().dropna(subset=[t])

    bestandsnaam = map / f"{t}_{jaar}.csv"
    df.to_csv(bestandsnaam)
