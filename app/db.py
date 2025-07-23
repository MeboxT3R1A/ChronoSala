# app/db.py
import pymysql
from flask import g

# Configurações (poderia vir do config.py, se quiser)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "port": 3307,
    "password": "senac",
    "database": "chronosala",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        try:
            db.close()
        except pymysql.err.Error:
            pass  # ignora erro de "already closed"
