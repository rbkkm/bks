import os
import re
import html

# --- CONFIGURATIE ---
SOURCE_DIR = r"C:\Je\Pad\Naar\HTML_Bestanden"
TARGET_DIR = r"C:\Je\Pad\Naar\Output"

# Maak de map aan als die niet bestaat
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

# REGEX UITLEG:
# <a[^>]*>      : Zoekt de openingstag en negeert attributen zoals href
# (.*?)         : Capture group 1: pakt alles tussen de tags (non-greedy)
# </a>          : Zoekt de sluit-tag
# re.DOTALL     : Zorgt dat de stip (.) ook nieuwe regels pakt
# re.IGNORECASE : Pakt zowel <a> als <A>
link_regex = re.compile(r"<a[^>]*>(.*?)</a>", re.DOTALL | re.IGNORECASE)


def process_files():
    processed_count = 0

    for root, dirs, files in os.walk(SOURCE_DIR):
        for filename in files:
            # Optioneel: filter op extensie
            if not filename.lower().endswith((".html", ".htm", ".txt")):
                continue

            file_path = os.path.join(root, filename)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Vind alle teksten binnen de a-tags
                matches = link_regex.findall(content)

                # Schoonmaak per match:
                # 1. HTML-entiteiten omzetten (&amp; naar &)
                # 2. Alle overige HTML tags binnen de link verwijderen
                # 3. Witruimte trimmen
                cleaned_matches = []
                for m in matches:
                    text = html.unescape(m)  # Zet &amp; etc. om
                    text = re.sub(r"<[^>]+>", "", text)  # Verwijder tags binnenin
                    text = " ".join(
                        text.split()
                    )  # Verwijder overtollige spaties/newlines
                    if text:
                        cleaned_matches.append(text)

                if cleaned_matches:
                    output_path = os.path.join(TARGET_DIR, f"{filename}.txt")
                    with open(output_path, "w", encoding="utf-8") as f_out:
                        f_out.write("\n".join(cleaned_matches))
                    processed_count += 1

            except Exception as e:
                print(f"Fout in {filename}: {e}")

    print(f"\nKlaar! {processed_count} bestanden succesvol verwerkt.")


if __name__ == "__main__":
    process_files()
