# app/routes/auth/services/auth_service.py
from app.db import get_db
from werkzeug.security import check_password_hash
import pymysql.cursors

def autenticar_usuario(usuario_input, senha_input):
    try:
        db = get_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        query = "SELECT email, nome, funcao, senha FROM funcionario WHERE email = %s OR matricula = %s"
        cursor.execute(query, (usuario_input, usuario_input))
        funcionario = cursor.fetchone()

        if funcionario and check_password_hash(funcionario['senha'], senha_input):
            return {
                'nome': funcionario['nome'],
                'funcao': funcionario['funcao'],
                'autenticado': True
            }
        else:
            return { 'autenticado': False }

    except Exception as e:
        raise Exception(f"Erro ao autenticar: {e}")


def buscar_funcionario_por_usuario(usuario):
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    query = "SELECT * FROM funcionario WHERE email = %s OR matricula = %s"
    cursor.execute(query, (usuario, usuario))
    return cursor.fetchone()

def verificar_senha(senha_digitada, senha_hash):
    return check_password_hash(senha_hash, senha_digitada)
