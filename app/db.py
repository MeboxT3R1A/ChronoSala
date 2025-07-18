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
    db = g.pop('db', None)
    if db is not None:
        db.close()
