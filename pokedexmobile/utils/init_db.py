import sqlite3

connection = sqlite3.connect('database.db')


connection.executescript(
"""DROP TABLE IF EXISTS favoris;

CREATE TABLE avoris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    id_pokemon INT NOT NULL
);"""
)


connection.commit()
connection.close()
