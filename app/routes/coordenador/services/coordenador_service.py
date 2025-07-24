# app/services/coordenador_service.py
#pensei em por dentro de uma pasta coordenador, pode?

import pymysql

def buscar_salas(conn):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM sala")
        return cursor.fetchall()

