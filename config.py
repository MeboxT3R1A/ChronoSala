# config.py
import os

# Define a base do diretório do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuração base para o aplicativo."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456789'

class DevelopmentConfig(Config):
    DEBUG = True 

class ProductionConfig(Config):
    DEBUG = False
