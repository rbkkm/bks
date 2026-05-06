import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

# for i in range(2003, 2026):
URL = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/"
print(URL)
# sys.exit()
# De URL van de webfolder
DOWNLOAD_MAP = "d:/data/w/d/d/zip"
EXTENSIE = ".zip"  # Filter op bestandstype (leeg laten voor alles)

# Maak de lokale map aan als deze nog niet bestaat
if not os.path.exists(DOWNLOAD_MAP):
    os.makedirs(DOWNLOAD_MAP)

# 1. Haal de HTML van de webmap op
response = requests.get(URL)
if response.status_code != 200:
    print(f"Fout: Kan pagina niet laden ({response.status_code})")

# 2. Zoek alle links (<a> tags) in de pagina
soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a")

for link in links:
    href = link.get("href")
    if not href:
        continue

    # Filter op extensie en negeer mappen (links die eindigen op /)
    if href.endswith(EXTENSIE) and not href.endswith("/"):
        # Maak een volledige URL van de relatieve link
        bestands_url = urljoin(URL, href)
        bestandsnaam = os.path.join(DOWNLOAD_MAP, href.split("/")[-1])

        # 3. Download het bestand
        print(f"Bezig met downloaden: {href}...")
        with requests.get(bestands_url, stream=True) as r:
            r.raise_for_status()
            with open(bestandsnaam, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

print("Klaar!")
