output_file = "d:/data/ecab/sd/SD_STAID000001.txt"
verwachte_kommas = 4
fouten = 0

with open(output_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        komma_count = line.count(",")
        if komma_count != verwachte_kommas:
            print(f"Regel {i} is incorrect: bevat {komma_count} komma's.")
            fouten += 1

        # Laat voortgang zien elke 100.000 regels
        if i % 100000 == 0:
            print(f"Gecontroleerd: {i} regels...")

if fouten == 0:
    print(
        f"\n✅ Perfect! Alle regels in {output_file} hebben exact {verwachte_kommas} komma's."
    )
else:
    print(f"\n❌ Klaar. Totaal aantal regels met fouten: {fouten}")
