import os
import re


def hernoem_bestanden():
    # De map waarin het script moet zoeken ('.' is de huidige map)
    map_pad = "."

    # Regex om het patroon te vinden: alles voor de 'split_' wordt verwijderd
    # Zoekt specifiek naar: ...split_ gevolgd door cijfers en .html
    patroon = re.compile(r".*split_(\d+\.html)$")

    print("Bestanden aan het hernoemen...")

    voor_bestanden = os.listdir(map_pad)
    hernoemd_aantal = 0

    for bestandsnaam in voor_bestanden:
        match = patroon.match(bestandsnaam)
        if match:
            nieuwe_naam = match.group(
                1
            )  # Dit pakt het gedeelte tussen de haakjes (000.html)

            try:
                os.rename(bestandsnaam, nieuwe_naam)
                print(f"Hernoemd: {bestandsnaam} -> {nieuwe_naam}")
                hernoemd_aantal += 1
            except FileExistsError:
                print(f"Fout: {nieuwe_naam} bestaat al, overgeslagen.")
            except Exception as e:
                print(f"Fout bij {bestandsnaam}: {e}")

    print(f"\nKlaar! {hernoemd_aantal} bestanden hernoemd.")


if __name__ == "__main__":
    hernoem_bestanden()
