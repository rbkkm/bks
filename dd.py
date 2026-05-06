import duckdb
import os

print(duckdb.__version__)


# Instellingen
BESTANDSNAAM = "mijn_data.parquet"
NIEUWE_DATA_BRON = "nieuwe_input.csv"  # Kan ook een andere .parquet of tabel zijn
TEMP_BESTAND = "temp_update.parquet"

con = duckdb.connect()

try:
    # Check of het basisbestand al bestaat
    if os.path.exists(BESTANDSNAAM):
        print(f"Bezig met samenvoegen van {BESTANDSNAAM}...")
        # Combineer oud + nieuw in een tijdelijk bestand
        con.execute(
            f"""
            COPY (
                SELECT * FROM '{BESTANDSNAAM}'
                UNION ALL
                SELECT * FROM '{NIEUWE_DATA_BRON}'
            ) TO '{TEMP_BESTAND}' (FORMAT PARQUET);
        """
        )

        # Vervang het oude bestand door het nieuwe (veilig)
        os.remove(BESTANDSNAAM)
        os.rename(TEMP_BESTAND, BESTANDSNAAM)
    else:
        print("Eerste keer: bestand wordt aangemaakt...")
        con.execute(
            f"COPY (SELECT * FROM '{NIEUWE_DATA_BRON}') TO '{BESTANDSNAAM}' (FORMAT PARQUET);"
        )

    print("Klaar! Bestand is nu ongeveer 500 MB.")

except Exception as e:
    print(f"Fout opgetreden: {e}")
    if os.path.exists(TEMP_BESTAND):
        os.remove(TEMP_BESTAND)
