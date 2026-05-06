"""
Python script voor vertaling html
ook voor checken dmv check prompt
ook voor imperial -> metric
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
with open("config/prmpt_g.json5", "r", encoding="utf-8") as file:
    prt = json5.load(file)

mdl = cfg["MODEL_G2"]

s_i = prt["PRM_C"]  # ccheck
s_i = prt["PRM_H"]  # vertaal

cts_s = stp_s = 9999

ptf = "D:/gthb/bks/tcw/en/OEBPS/xhtml/*.*"
pto = "D:/gthb/bks/tcw/nl/"

bgn = "c003"  # begin filename
end = "c003"

end += "z"  # end filename
tgv = prt = 0
os.makedirs(pto, exist_ok=True)

# start file processing

f_list = natsorted(glob.glob(ptf))

for f_name in f_list:

    rslt = ""

    if bgn < os.path.basename(f_name) < end:

        print("Time:", datetime.now().strftime("%H:%M:%S"))

        with open(f_name, "r", encoding="utf-8") as f:
            full_text = f.read()

        all_lns = full_text.splitlines()

        lns = len(all_lns)

        for i in range(0, lns):
            all_lns[i] = all_lns[i].strip()

        cts = ""

        for i in range(0, lns, stp_s):

            s_x = i
            e_x = i + cts_s

            cts = "\n".join(all_lns[s_x:e_x])

            if not cts or s_x >= lns:
                break
            cts = full_text
            client = genai.Client(api_key=GK)

            cfg = types.GenerateContentConfig(system_instruction=s_i)

            try:
                rp = client.models.generate_content(
                    model=mdl,
                    config=cfg,
                    contents=cts,
                )
            except Exception as e:
                logging.info(f"Geen rslt request {e} {f_name} {e_x}")
                sys.exit()

            rt = rp.text

            prt += 1

            print("Time:", datetime.now().strftime("%H:%M:%S"))

            cf = pto + str(Path(os.path.basename(f_name)).with_suffix("")) + ".txt"
            tf = pto + os.path.basename(f_name)
            print(tf)
            with open(
                tf,
                "w",
                encoding="utf-8",
            ) as f_uit:
                f_uit.write(rt)

# end f_list loop
logging.info(f"ready.  prt:{prt}")
print(f"ready. prt:{prt}")
