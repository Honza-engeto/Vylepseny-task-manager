import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pluton11",
        database="sys"
    )
    print("Pripojeni probehlo uspesne.")
except mysql.connector.Error as err:
    print(f"Chyba pri pripojeni: {err}")

# kurzor
cursor = conn.cursor()

# vytvoreni tabulky ukoly
try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(100),
            popis VARCHAR(100),
            stav VARCHAR(10),
            datum_vytvoreni DATE
        )
    ''')
    print("Tabulka byla vvytvorena.")
except mysql.connector.Error as err:
    print(f"Chyba behem vytvareni tabulky: {err}")

    # vlozeni zaznamu
data = [
    ('Ukol1', 'Popis1', 'whatever', '2025-09-01')
]
try:
    cursor.executemany("INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni) VALUES (%s, %s, %s, %s)", data)
    conn.commit()
    print("Zaznam vlozen")
except mysql.connector.Error as err:
    print(f"Chyba pri ukladani dat: {err}")

# uzavření pripojeni
cursor.close()
conn.close()
print("Pripojeni k databazi bylo uzavreno.")