# app/db.py
import pymysql
from flask import g
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "port": 3306,
    "password": "lasanha",
    "database": "chronosala",
    "port": 3306,
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
    "connect_timeout": 10  # Adicionado timeout
}

def get_db():
    """Obtém uma conexão com o banco de dados"""
    if not hasattr(g, 'db'):
        try:
            logger.debug("Tentando conectar ao banco de dados...")
            g.db = pymysql.connect(**DB_CONFIG)
            logger.info("Conexão com o banco estabelecida com sucesso")
        except pymysql.err.OperationalError as e:
            logger.error(f"Erro de conexão: {e}")
            raise RuntimeError("Não foi possível conectar ao banco de dados") from e
    return g.db

def close_db(e=None):
    """Fecha a conexão com o banco de dados"""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, params=(), fetchone=False, fetchall=False):
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    result = cursor.fetchone() if fetchone else cursor.fetchall() if fetchall else None
    db.commit()
    return result
