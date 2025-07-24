# app/routes/auth/services/auth_service.py
from app.db import execute_query
from werkzeug.security import check_password_hash

def autenticar_login(usuario_input, senha_input):
    funcionario = buscar_funcionario_por_usuario(usuario_input)
    if funcionario and verificar_senha(senha_input, funcionario['senha']):
        return {
            'nome': funcionario['nome'],
            'funcao': funcionario['funcao'],
            'senha': funcionario['senha']
        }
    return None

def buscar_funcionario_por_usuario(usuario):
    query = "SELECT * FROM funcionario WHERE email = %s OR matricula = %s"
    return execute_query(query, (usuario, usuario), fetchone=True)

def verificar_senha(senha_digitada, senha_hash):
    return check_password_hash(senha_hash, senha_digitada)
