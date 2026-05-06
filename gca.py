"""
Python script voor vertaling html
ook voor checken dmv check prompt
"""

from datetime import datetime
import os, warnings, glob, logging
from pathlib import Path
from natsort import natsorted
import json
import json5
from dotenv import load_dotenv
from google import genai
from google.genai import types
from logging.handlers import TimedRotatingFileHandler
from pprint import pprint
import time
import sys
import re

logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("google_genai.models").setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore", category=UserWarning)

# 1. Definieer het logbestand en de instellingen

LOG_DIR = Path("logs")
LOG_FILENAME = "g.log"
LOG_FULL_PATH = LOG_DIR / LOG_FILENAME

LOG_DIR.mkdir(parents=True, exist_ok=True)

# --- Hoofdlogger Configuratie ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- 1. File Handler (TimedRotatingFileHandler) ---
handler = TimedRotatingFileHandler(
    filename=LOG_FULL_PATH,
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
)
handler.suffix = "%Y-%m-%d"

# De Formatter voor de file handler:
# Belangrijk: Voeg 'datefmt' toe met alleen H:M:S (geen ,SSS)
FILE_FORMATTER = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",  # <-- DE OPLOSSING: Zonder milliseconden
)

handler.setFormatter(FILE_FORMATTER)
logger.addHandler(handler)

# --- 2. Console Handler (StreamHandler) ---
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)

# De Formatter voor de console handler:
# %(asctime)s wordt hier niet gebruikt, maar voor consistentie behouden
CONSOLE_FORMATTER = logging.Formatter(
    fmt="%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(CONSOLE_FORMATTER)

# Voeg de console handler toe (gebruik 'logger.addHandler(console_handler)' in plaats van logging.getLogger().addHandler)
# Het gebruik van logging.getLogger() zonder naam is equivalent aan logger
logger.addHandler(console_handler)
load_dotenv()
GK = os.getenv("GEMINI_API_KEY")

with open("config/cfg_g.json5", "r", encoding="utf-8") as file:
    cfg = json5.load(file)
with open("config/prmpt_en.json5", "r", encoding="utf-8") as file:
    prt = json5.load(file)

mdl = cfg["MODEL_G2"]

s_i = prt["PRM_C"]
s_i = prt["PRM_T"]
ptf = r"D:\gthb\md\*.md"

pto = r"D:\gthb\md\\"

bgn = ""
end = ""
end += "z"
# begin filename


prt = 0


sf = ""
sf = ".c.txt"
# start file processing

Path(pto).mkdir(parents=True, exist_ok=True)

f_list = natsorted(glob.glob(ptf))

for f_name in f_list:

    if bgn <= str(Path(os.path.basename(f_name)).with_suffix("")) <= end:

        print("Time:", datetime.now().strftime("%H:%M:%S"), os.path.basename(f_name))

        with open(f_name, "r", encoding="utf-8") as f:
            cts = f.read()

        client = genai.Client(api_key=GK)
        cfg = types.GenerateContentConfig(system_instruction=s_i)

        try:
            rp = client.models.generate_content(
                model=mdl,
                config=types.GenerateContentConfig(system_instruction=s_i),
                contents=cts,
            )
        except Exception as e:
            logging.info(f"No rp  {e} {os.path.basename(f_name)} ")
            sys.exit()

        rt = rp.text

        prt += 1

        print("Time:", datetime.now().strftime("%H:%M:%S"))

        wt = pto + os.path.basename(f_name) + sf

        with open(
            wt,
            "w",
            encoding="utf-8",
        ) as f_uit:
            f_uit.write(rt)

# end f_list loop
logging.info(f"ready.  prt:{prt}")
print(f"ready. prt:{prt}")
