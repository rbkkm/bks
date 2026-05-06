import requests
import zipfile
import io, sys
import pandas as pd
import sqlite3

url = "https://api.ned.nl/v1/utilizations"

headers = {
    "X-AUTH-TOKEN": "576e5fe818d9464fd58c4e99eac786ae1e358217fcf6233e3dd6cb1cc7a4fd30",
    "accept": "application/ld+json",
}
params = {
    "point": 0,
    "type": 2,
    "granularity": 8,
    "granularitytimezone": 1,
    "classification": 2,
    "activity": 1,
    "validfrom[strictly_before]": "2025-11-17",
    "validfrom[after]": "2023-11-16",
}
response = requests.get(url, headers=headers, params=params, allow_redirects=False)

print(response.text)
