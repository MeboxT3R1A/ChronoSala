from app.db import get_db
import pymysql


def buscar_funcionarios(busca=None, filtro_funcao=None):
    conn = get_db()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        query = "SELECT * FROM funcionario WHERE 1=1"
        params = []

        if busca:
            query += " AND (nome LIKE %s OR matricula = %s)"
            params.extend((f"%{busca}%", busca))

        if filtro_funcao:
            query += " AND funcao = %s"
            params.append(filtro_funcao)

        cursor.execute(query, params)
        return cursor.fetchall()


def buscar_funcionario_por_email(email):
    conn = get_db()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM funcionario WHERE email=%s", (email,))
        return cursor.fetchone()


def atualizar_funcionario(email, nome, matricula, senha, funcao):
    conn = get_db()
    with conn.cursor() as cursor:
        query = """
            UPDATE funcionario
            SET nome=%s, matricula=%s, senha=%s, funcao=%s
            WHERE email=%s
        """
        cursor.execute(query, (nome, matricula, senha, funcao, email))
        conn.commit()


def cadastrar_funcionario(email, nome, matricula, senha, funcao):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO funcionario (email, nome, matricula, senha, funcao)
            VALUES (%s, %s, %s, %s, %s)
        """, (email, nome, matricula, senha, funcao))
        conn.commit()
