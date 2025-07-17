# config.py
import os

# Define a base do diretório do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Chave secreta para segurança da sessão, formulários CSRF, etc.
    # É CRUCIAL que esta chave seja ÚNICA e SECRETA em produção.
    # Em produção, use uma variável de ambiente: os.environ.get('SECRET_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456789'

    # Configuração do banco de dados para Flask-SQLAlchemy
    # Formato para MySQL com PyMySQL (recomendado): mysql+pymysql://user:password@host:port/database_name
    # Use variáveis de ambiente em produção para as credenciais do DB
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:senac@localhost:3307/ChronoSala'

    # Desativa o rastreamento de modificações, o que economiza memória.
    # Se você não precisar de sinais do SQLAlchemy sobre mudanças nos objetos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Outras configurações que você possa adicionar no futuro, como e-mail, upload, etc.
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # ...

class DevelopmentConfig(Config):
    DEBUG = True # Ativa o modo de depuração para desenvolvimento
    # Em desenvolvimento, você pode ter um banco de dados local diferente, por exemplo:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dev_user:dev_pass@localhost:3306/dev_db'

class ProductionConfig(Config):
    DEBUG = False # Desativa o modo de depuração em produção
    # Em produção, é essencial que DATABASE_URL e SECRET_KEY venham de variáveis de ambiente
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SECRET_KEY = os.environ.get('SECRET_KEY')

# Você pode adicionar mais classes de configuração (e.g., TestingConfig)