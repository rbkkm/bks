import os

"""
    Wijzigt het voorvoegsel van bestanden in een opgegeven map.

    Args:
        directory_path (str): Het pad naar de map met de bestanden.
        old_prefix (str): Het te vervangen voorvoegsel.
        new_prefix (str): Het nieuwe voorvoegsel.
"""
directory_path = r"D:\gthb\dwo\OEBPS\Text"  # Gebruik r'' voor Windows-paden
old_prefix = "Section"
new_prefix = ""

print(f"Start van hernoemen in: {directory_path}")

# Doorloop alle bestanden in de map
for filename in os.listdir(directory_path):
    # Controleer of het bestand het oude voorvoegsel heeft
    if filename.startswith(old_prefix):
        # Creëer de nieuwe bestandsnaam door het oude voorvoegsel te vervangen
        new_filename = (
            new_prefix + filename[len(old_prefix) :]  # + ".xhtml"
        )  # filename[len(old_prefix) :]
        print(new_filename)
        new_filename = new_filename.replace("html", "xhtml")
        # Volledige paden voor bron (src) en bestemming (dst)
        src = os.path.join(directory_path, filename)
        dst = os.path.join(directory_path, new_filename)

        try:
            # Hernoem het bestand
            os.rename(src, dst)
            print(f"Hernoemd: {filename} -> {new_filename}")
        except OSError as e:
            print(f"Fout bij hernoemen van {filename}: {e}")

print("Hernoemen voltooid.")

# --- Gebruiksvoorbeeld ---
# Zorg ervoor dat u het juiste pad en de juiste voorvoegsels invult
