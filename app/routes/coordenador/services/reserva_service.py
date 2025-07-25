# app/routes/coordenador/services/reserva_service.py
from flask import request
from app.db import get_db
import pymysql

def buscar_reservas(nome_sala, data_res, busca, conn):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        query = "SELECT * FROM reserva"
        filtros = []
        valores = []

        if nome_sala:
            filtros.append("nome_sala = %s")
            valores.append(nome_sala)
        if data_res:
            filtros.append("data_res = %s")
            valores.append(data_res)

        if busca:
            if busca.isdigit():
                filtros.append("(id_res = %s OR nome_sala LIKE %s OR email LIKE %s)")
                valores.extend([int(busca), f"%{busca}%", f"%{busca}%"])
            else:
                filtros.append("(nome_sala LIKE %s OR email LIKE %s)")
                valores.extend([f"%{busca}%", f"%{busca}%"])

        if filtros:
            query += " WHERE " + " AND ".join(filtros)
        query += " ORDER BY data_res DESC, inicio ASC"

        cursor.execute(query, valores)
        return cursor.fetchall()

def extrair_filtros_request():
    return {
        "nome_sala": request.args.get('sala'),
        "data_res": request.args.get('data'),
        "busca": request.args.get('busca'),
    }

def buscar_reservas_filtradas(nome_sala=None, data_res=None, busca=None):
    conn = get_db()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        query = "SELECT * FROM reserva"
        filtros = []
        valores = []

        if nome_sala:
            filtros.append("nome_sala = %s")
            valores.append(nome_sala)
        if data_res:
            filtros.append("data_res = %s")
            valores.append(data_res)
        if busca:
            if busca.isdigit():
                filtros.append("(id_res = %s OR nome_sala LIKE %s OR email LIKE %s)")
                valores.extend([int(busca), f"%{busca}%", f"%{busca}%"])
            else:
                filtros.append("(nome_sala LIKE %s OR email LIKE %s)")
                valores.extend([f"%{busca}%", f"%{busca}%"])

        if filtros:
            query += " WHERE " + " AND ".join(filtros)
        query += " ORDER BY data_res DESC, inicio ASC"

        cursor.execute(query, valores)
        return cursor.fetchall()

def criar_reserva(nome_sala, email, data_res, inicio, termino):
    conn = get_db()
    with conn.cursor() as cursor:
        query = """
            INSERT INTO reserva (nome_sala, email, data_res, inicio, termino, status_res, status_chave)
            VALUES (%s, %s, %s, %s, %s, 'reservado', 'pendente')
        """
        cursor.execute(query, (nome_sala, email, data_res, inicio, termino))
        conn.commit()

def marcar_chave_entregue(id_res):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE reserva SET status_chave = 'Chave retirada' WHERE id_res = %s", (id_res,))
        conn.commit()

def marcar_chave_devolvida(id_res):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE reserva SET status_chave = 'Chave devolvida' WHERE id_res = %s", (id_res,))
        conn.commit()

def cancelar_reserva(id_res):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE reserva SET status_res = 'cancelado' WHERE id_res = %s AND status_chave = 'pendente'",
            (id_res,)
        )
        conn.commit()

def buscar_nomes_salas():
    conn = get_db()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT nome_sala FROM sala")
        resultado = cursor.fetchall()
        return [row['nome_sala'] for row in resultado]
