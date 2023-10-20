import sqlite3

# Création des tables

try:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE USER (id INTEGER, login TEXT NOT NULL, mdp TEXT NOT NULL)")
    con.commit()
except sqlite3.OperationalError:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    con.close()

try:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE FAVORI (id_user INTEGER, id_pokemon INTEGER NOT NULL , FOREIGN KEY (id_user) REFERENCES USER (id))")
    con.commit()
except sqlite3.OperationalError:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    con.close()