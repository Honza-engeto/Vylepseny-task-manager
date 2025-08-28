ukoly = []

def hlavni_menu():
    while True:
        print("\nSpravce ukolu")
        print("1) Pridat ukol")
        print("2) Zobrazit vsechny ukoly")
        print("3) Odstranit ukol")
        print("4) Konec programu")
        volba = input("Vyberte moznost (1-4): ")

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            odstranit_ukol()
        elif volba == "4":
            print("Konec programu")
            break
        else:
            print("Neplatna volba")

def pridat_ukol():
    while True:
        nazev = input("Zadejte nazev ukolu: ")
        popis = input("Zadejte popis ukolu: ")
        if not nazev or not popis:
            print("Nazev ani popis nesmi byt prazdny")
            continue
        ukoly.append({"nazev": nazev, "popis": popis})
        print(f"Ukol '{nazev}' pridan.")
        print(ukoly)
        return  # zpet do menu

def zobrazit_ukoly():
    if not ukoly:
        print("Seznam ukolu je prazdny.")
        return
    print("\nSeznam ukolu:")
    for i, u in enumerate(ukoly, start=1):
        print(f"{i}. {u['nazev']} – {u['popis']}")

def odstranit_ukol():
    if not ukoly:
        print("Seznam je prazdny.")
        return

    # aktualni úkoly
    zobrazit_ukoly()

    volba = input("Zadejte cislo ukolu k odstraneni (Enter = zrusit): ").strip()
    if volba == "":
        print("Mazani zruseno.")
        return
    if not volba.isdigit():
        print("Musite zadat cislo.")
        return

    idx = int(volba)
    if not (1 <= idx <= len(ukoly)):
        print("Ukol neexistuje.")
        return

    smazany = ukoly.pop(idx - 1)
    print(f"Smazan ukol: {smazany['nazev']}")

if __name__ == "__main__":
    hlavni_menu()
