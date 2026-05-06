import os
import requests
from bs4 import BeautifulSoup
import sys

# for i in range(2003, 2026):
url = "https://ned.nl/system/files/datasets/WKK-uur-voorspelling-aankomende-uren.csv"
print(url)
# sys.exit()
# De URL van de webfolder
DOWNLOAD_MAP = "d:/data/w/d/d/zip"
EXTENSIE = ".zip"  # Filter op bestandstype (leeg laten voor alles)

# Maak de lokale map aan als deze nog niet bestaat
if not os.path.exists(DOWNLOAD_MAP):
    os.makedirs(DOWNLOAD_MAP)

# 1. Haal de HTML van de webmap op
response = requests.get(url)
if response.status_code != 200:
    print(f"Fout: Kan pagina niet laden ({response.status_code})")


# 3. Download het bestand
print(f"Bezig met downloaden: ...")
with requests.get(url, stream=True) as r:
    r.raise_for_status()
    # with open(bestandsnaam, "wb") as f:
    #    for chunk in r.iter_content(chunk_size=8192):
    #        f.write(chunk)

print("Klaar!")
