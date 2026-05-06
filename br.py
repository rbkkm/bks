import math


def lengte_graad_berekenen(breedtegraad):
    # De afstand van 1 graad op de evenaar in kilometers
    afstand_evenaar = 111.319444444

    # Stap 1: Zet de breedtegraad om van graden naar radialen
    radialen = math.radians(breedtegraad)

    # Stap 2: Bereken de krimpfactor met de cosinus
    afstand = afstand_evenaar * math.cos(radialen)

    return afstand


# Voorbeelden
locaties = [0, 10, 40, 50, 60]

for b in locaties:
    resultaat = lengte_graad_berekenen(b) / 4
    print(f"Op {b}° NB/ZB is 1 graad lengtegraad: {resultaat:.3f} km")
