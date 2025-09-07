import sys
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Pluton11",
    "database": "sys",
    "autocommit": True,
}

TABLE_NAME = "ukoly"
ALLOWED_STATES = ("Nezahajeno", "Probiha", "Hotovo")


# 1) pripojeni_db() - pripojeni k databayi
def pripojeni_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Chyba pripojeni k DB: {e}")
        sys.exit(1)


# 2) vytvoreni_tabulky() - vytvori tabulku, pokud neexistuje
def vytvoreni_tabulky(conn):
    sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nazev VARCHAR(255) NOT NULL,
        popis TEXT NOT NULL,
        stav ENUM('Nezahajeno','Probiha','Hotovo') NOT NULL DEFAULT 'Nezahajeno'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    with conn.cursor() as cur:
        cur.execute(sql)


# 3) hlavni_menu() - hlavni nabidka
def hlavni_menu(conn):
    while True:
        print("\nSpravce ukolu")
        print("1) Pridat ukol")
        print("2) Zobrazit ukoly")
        print("3) Aktualizovat stav ukolu")
        print("4) Odstranit ukol")
        print("5) Konec programu")
        volba = input("Vyberte moznost (1-5): ").strip()

        if volba == "1":
            pridat_ukol(conn)
        elif volba == "2":
            zobrazit_ukoly(conn)
        elif volba == "3":
            aktualizovat_ukol(conn)
        elif volba == "4":
            odstranit_ukol(conn)
        elif volba == "5":
            print("Konec programu.")
            break
        else:
            print("Neplatna volba, zkuste znovu.")


# 4) pridat_ukol() - pridani ukolu (nazev a popis povinne)
def pridat_ukol(conn):
    while True:
        nazev = input("Zadejte nazev ukolu: ").strip()
        popis = input("Zadejte popis ukolu: ").strip()
        if not nazev or not popis:
            print("Nazev i popis jsou povinne, nesmi byt prazdne.")
            continue

        sql = f"INSERT INTO {TABLE_NAME} (nazev, popis, stav) VALUES (%s, %s, %s)"
        with conn.cursor() as cur:
            cur.execute(sql, (nazev, popis, "Nezahajeno"))
            new_id = cur.lastrowid
        print(f"Ukol #{new_id} '{nazev}' pridan se stavem Nezahajeno.")
        return


# 5) zobrazit_ukoly() - seznam ukolu s volitelnym filtrem stavu
def zobrazit_ukoly(conn):
    print("\nFiltr stavu: A) Vse B) Nezahjaeno C) Probiha D) Hotovo")
    choice = input("Vyberte filtr (A/B/C/D, Enter=Vse): ").strip().upper()

    stav_filter = None
    if choice == "B":
        stav_filter = "Nezahajeno"
    elif choice == "C":
        stav_filter = "Probiha"
    elif choice == "D":
        stav_filter = "Hotovo"

    if stav_filter:
        sql = f"SELECT id, nazev, popis, stav FROM {TABLE_NAME} WHERE stav=%s ORDER BY id"
        params = (stav_filter,)
    else:
        sql = f"SELECT id, nazev, popis, stav FROM {TABLE_NAME} ORDER BY id"
        params = ()

    with conn.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    if not rows:
        print("Zadne ukoly nebyly nalezeny.")
        return

    print("\nSeznam ukolu:")
    for r in rows:
        print(f"[{r['id']}] {r['nazev']} - {r['popis']} (stav: {r['stav']})")


# 6) aktualizovat_ukol() - zmena stavu ukolu podle ID
def aktualizovat_ukol(conn):
    zobrazit_ukoly(conn)
    raw = inpit("\nZadejte ID ukolu, ktery chcete aktualizovat (Enter=zrusit): ").strip()
    if raw == "":
        print("Aktualizace zrusena.")
        return
    if not raw.isdigit():
        print("Musite zadat cislo ID.")
        return
    task_id = int(raw)

    print("Dostupne stavy: 1) Nezahajeno  2) Probiha  3) Hotovo")
    stav_choice = input("Vyberte novy stav (1-3): ").strip()
    mapping = {"1": "Nezahajeno", "2": "Probiha", "3": "Hotovo"}
    if stav_choice not in mapping:
        print("Neplatna volba stavu.")
        return
    new_state = mapping[stav_choice]

    sql = f"UPDATE {TABLE_NAME} SET stav=%s WHERE id=%s"
    with conn.cursor() as cur:
        cur.execute(sql, (new_state, task_id))
        if cur.rowcount == 0:
            print("Ukol s danym ID neexistuje.")
            return
    print(f"Ukol #{task_id} aktualizovan na stav: {new_state}.")


# 7) odstranit_ukol() - smazani ukolu podle ID
def odstranit_ukol(conn):
    zobrazit_ukoly(conn)
    raw = input("\nZadejte ID ukolu k odstraneni (Enter=zrusit): ").strip()
    if raw == "":
        print("Mazani zruseno.")
        return
    if not raw.isdigit():
        print("Musite zadat cislo ID.")
        return
    task_id = int(raw)

    sql = f"DELETE FROM {TABLE_NAME} WHERE id=%s"
    with conn.cursor() as cur:
        cur.execute(sql, (task_id,))
        if cur.rowcount == 0:
            print("Ukol s danym ID neexistuje.")
            return
    print(f"Ukol #{task_id} byl odstranen.")


if __name__ == "__main__":
    conn = pripojeni_dv()
    vytvoreni_tabulky(conn)
    try:
        hlavni_menu(conn)
    finally:
        try:
            conn.close()
        except Exception:
            pass