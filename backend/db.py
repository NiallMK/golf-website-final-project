import sqlite3

def get_db():
    conn = sqlite3.connect("golf-website.db")
    conn.row_factory = sqlite3.Row

    #required for foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn

