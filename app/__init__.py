from flask import Flask
from app.routes.coordenador import coordenador
from app.routes.instrutor import instrutor
from app.routes.geral import geral

def create_app():
    app = Flask(__name__)
    app.secret_key = '1234567890abcdef'

    app.register_blueprint(geral)
    app.register_blueprint(coordenador, url_prefix='/coordenador')
    app.register_blueprint(instrutor, url_prefix='/instrutor')
    return app