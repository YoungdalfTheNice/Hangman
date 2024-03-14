import sqlite3
from random import choice

MAX_VERSUCHE = 5

connection = sqlite3.connect("database.db")
cur = connection.cursor()

cur.execute("SELECT Count(*) FROM words")
rows = cur.fetchone()[0]

buchstaben = int(input("Bitte gib die Anzahl an Buchstaben ein, die das Wort haben soll: "))
wort = ""

# Wähle zufälliges Wort aus der Datenbank mit der gewünschten Anzahl von Buchstaben
while len(wort) != buchstaben:
    randomrow = choice(range(1, rows + 1))
    cur.execute("SELECT word FROM words WHERE rowid = ?", (randomrow,))
    wort = cur.fetchone()[0]

versuch = ["_"] * buchstaben
positionen = []

while MAX_VERSUCHE > 0:
    print("".join(versuch))
    
    buchstabe = input("Bitte tippe einen Buchstaben, der im Wort vorkommen soll: ").lower()

    if len(buchstabe) != 1 or not buchstabe.isalpha():
        print("Ungültige Eingabe. Bitte gib einen einzelnen Buchstaben ein.")
        continue

    if buchstabe in positionen:
        print("Du hast diesen Buchstaben bereits geraten.")
        continue

    if buchstabe in wort.lower():
        positionen.extend([i for i, letter in enumerate(wort.lower()) if letter == buchstabe])
        for position in positionen:
            versuch[position] = wort[position]
    else:
        MAX_VERSUCHE -= 1
        print(f"Falsch! Du hast noch {MAX_VERSUCHE} Versuche übrig.")

    if "_" not in versuch:
        print(f"Korrekt! Das gesuchte Wort ist {wort}")
        break

if "_" in versuch:
    print(f"Spiel verloren. Das gesuchte Wort wäre {wort} gewesen.")

connection.close()
