# app/__init__.py
from flask import Flask, redirect, url_for
from app.db import close_db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')  # Carrega configurações do config.py

    # Importa blueprints
    from app.routes.geral import geral_bp
    from app.routes.auth import login_bp
    from app.routes.coordenador import coordenador_bp
    from app.routes.instrutor import instrutor_bp

    # Registra os blueprints
    app.register_blueprint(geral_bp)         # '/' → Rotas públicas
    app.register_blueprint(login_bp)         # '/login'
    app.register_blueprint(coordenador_bp)   # '/coordenador'
    app.register_blueprint(instrutor_bp)     # '/instrutor'

    # Fecha conexão com banco ao encerrar a requisição
    app.teardown_appcontext(close_db)

    # Redireciona '/' para a home pública
    @app.route('/')
    def index():
        return redirect(url_for('geral_bp.home'))

    return app
