# app/routes/coordenador/services/coordenador_service.py

from app.db import get_db
import pymysql

def buscar_salas():
    conn = get_db()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM sala")
        return cursor.fetchall()
