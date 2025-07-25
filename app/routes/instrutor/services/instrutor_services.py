# app/routes/instrutor/services/instrutor_service.py

from app.db import get_db
import pymysql.cursors

def obter_salas_com_reservas():
    conn = get_db()
    with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM sala")
        salas = cursor.fetchall()

        for sala in salas:
            cursor.execute("SELECT r.*, s.nome_sala FROM reserva r JOIN sala s ON r.id_sala = s.id_sala WHERE s.nome_sala = %s", (sala['nome_sala'],))
            sala['reservas'] = cursor.fetchall()

    return salas
