import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="USUARIO_AQUI",
        password="SENHA_AQUI",
        database="NOME_DO_BANCO",
        port=3306
    )
