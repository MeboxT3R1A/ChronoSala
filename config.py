# config.py
import os

# Define a base do diretório do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuração base para o aplicativo."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456789'

class DevelopmentConfig(Config):
    DEBUG = True
    # Adicione estas configurações
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'lasanha'
    DB_NAME = 'chronosala'
    DB_PORT = 3306

class ProductionConfig(Config):
    DEBUG = False
