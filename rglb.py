from pathlib import Path
import pandas as pd

# Vul hier de map in die je wilt doorzoeken
map_pad = Path("d:/dwnld/ecab")
unieke_kolom = "STAID"
bestanden = list(map_pad.rglob("stations.txt"))
df_hoofd = pd.read_csv(bestanden[0], skiprows=17, on_bad_lines="skip").set_index(
    unieke_kolom
)
df_hoofd = df_hoofd.map(lambda x: x.strip() if isinstance(x, str) else x)
df_hoofd.columns = df_hoofd.columns.str.strip()

for pad in bestanden[1:]:
    print(pad)
    df_n = pd.read_csv(pad, skiprows=17, on_bad_lines="skip").set_index(unieke_kolom)
    df_n = df_n.map(lambda x: x.strip() if isinstance(x, str) else x)
    df_n.columns = df_n.columns.str.strip()
    # Filter: pak alleen rijen waarvan de index NIET in df_hoofd zit
    nieuwe_rijen = df_n[~df_n.index.isin(df_hoofd.index)]
    if not nieuwe_rijen.empty:
        df_hoofd = pd.concat([df_hoofd, nieuwe_rijen])

df_hoofd = df_hoofd.sort_index(ascending=True)
b = "d:/dwnld/ecab/cln/stn.csv"
df_hoofd.reset_index().to_csv(b, index=False)
