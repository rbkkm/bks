"""
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import gspread

# Connect naar je Parquet
con = duckdb.connect()

# Haal data op als een Arrow-object (Zero-copy!)
arrow_table = con.execute("SELECT * FROM 'd:/Data/w/wmoid.parquet'").arrow()

# Nu heb je de data in 'arrow_table' zonder dat het geheugen dubbel belast wordt.
print(arrow_table)


# --- STAP 1: Data inladen in Arrow-formaat ---
# Stel je leest een Parquet bestand (Arrow op schijf)
table = pq.read_table("data.parquet")

# Of je leest direct uit een database die Arrow ondersteunt (zoals DuckDB of Snowflake)
# table = connection.execute("SELECT * FROM data").fetch_arrow_table()

# --- STAP 2: Voorbereiden voor Sheets ---
# We halen de headers op
headers = table.schema.names

# We converteren de Arrow-batches direct naar een lijst van rijen
# Dit is veel lichter voor je geheugen dan een Pandas DataFrame
rows = table.to_pylist()
data_to_push = [headers] + [[row[col] for col in headers] for row in rows]

# --- STAP 3: Schrijven naar Google Sheets ---
gc = gspread.service_account(filename="creds.json")
sh = gc.open("Mijn_Dashboard").sheet1
sh.update("A1", data_to_push)

"""

import pyarrow as pa
import pyarrow.parquet as pq
import duckdb
import gspread
from google.oauth2 import service_account

# 1. Authenticatie met de moderne Google-auth library
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = service_account.Credentials.from_service_account_file(
    "d:/data/gen-lang-client.json", scopes=SCOPES
)

client = gspread.authorize(creds)
# sheet = client.create("wmo")
# sheet.share("rsvanbekkum@gmail.com", perm_type="user", role="writer")
sheet = client.open("wmo").sheet1

# 2. DuckDB -> Arrow
con = duckdb.connect(":memory:")  # Of je .db bestand
arrow_table = con.execute(
    "SELECT * FROM read_parquet('d:/data/w/wmo.parquet') "
).to_arrow_table()

# 3. Arrow -> List of Lists (Directe injectie)
# We gebruiken to_pydict() omdat dit vaak sneller is in de conversie naar rijen
data_dict = arrow_table.to_pydict()
headers = arrow_table.schema.names

# We bouwen de rijen op door over de lengte van de kolommen te itereren
# rows = []
# for i in range(len(arrow_table)):
#    rows.append([data_dict[col][i] for col in headers])

rows = arrow_table.to_pylist()
data_to_push = [headers] + [[row[col] for col in headers] for row in rows]

# 4. Update de sheet in één keer

sheet.update(data_to_push, range_name="A1")
