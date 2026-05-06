import pandas as pd


def dms_naar_decimaal(waarde):
    # Als de waarde al een getal is of leeg (NaN), sla over
    if pd.isna(waarde) or not isinstance(waarde, str):
        return waarde

    # STAP 1: Trim de tekst (spaties aan begin/eind verwijderen)
    s = waarde.strip()

    try:
        # Splits op dubbele punt
        delen = s.split(":")
        if len(delen) < 3:
            return s  # Geen geldig DMS formaat, geef origineel terug

        d = float(delen[0])
        m = float(delen[1])
        s = float(delen[2])

        if delen[0][0] == "-":
            dd = d - (m / 60) - (s / 3600)
        else:
            dd = d + (m / 60) + (s / 3600)

        return f"{dd:.3f}"
    except (ValueError, IndexError):
        return s


# 1. Lees het bestand in
df = pd.read_csv("d:/data/ecad/s_sd.csv")

# 2. Trim de KOLOMNAMEN (headers)
# Dit haalt spaties weg in "  LAT" zodat het gewoon "LAT" wordt
df.columns = df.columns.str.strip()

# 3. Trim de DATA en Converteer
# We passen de functie toe op de relevante kolommen
df["LAT"] = df["LAT"].apply(dms_naar_decimaal)
df["LON"] = df["LON"].apply(dms_naar_decimaal)

# Optioneel: Trim ook alle andere tekstkolommen (zoals STANAME en CN)
df["STANAME"] = df["STANAME"].str.strip()
df["CN"] = df["CN"].str.strip()

# 4. Sla op
df.to_csv("d:/3stations_schoon.csv", index=False)

print("Bestand succesvol getrimd en geconverteerd naar 'stations_schoon.csv'.")
