# db.py - gives safe access to DB
import sqlite3

DATABASE = "golf-website.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
