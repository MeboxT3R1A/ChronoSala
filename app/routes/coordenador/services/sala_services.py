# app/routes/coordenador/services/sala_service.py

import pymysql
from app.db import get_db

def buscar_sala_por_nome(nome_sala):
    conn = get_db()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM sala WHERE nome_sala=%s", (nome_sala,))
        return cursor.fetchone()

def atualizar_status_sala(nome_sala, novo_status):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE sala SET status_sala=%s WHERE nome_sala=%s",
            (novo_status, nome_sala)
        )
        conn.commit()

def excluir_sala_por_nome(nome_sala):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM sala WHERE nome_sala = %s", (nome_sala,))
        conn.commit()

def adicionar_sala_db(nome_sala, status_sala):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO sala (nome_sala, status_sala) VALUES (%s, %s)",
            (nome_sala, status_sala)
        )
        conn.commit()
