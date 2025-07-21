# app/__init__.py
from flask import Flask, render_template, redirect, url_for 
from app.db import close_db  

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig') # Carrega as configurações do config.py

    # Importa e registra os blueprints

    from app.routes.coordenador import coordenador_bp
    from app.routes.instrutor import instrutor_bp
    from app.routes.geral import geral_bp
    from app.routes.auth import login_bp # Importa o blueprint de autenticação

    # Registrar blueprints no aplicativo.

    app.register_blueprint(geral_bp) # Geral não tem prefixo, suas rotas são na raiz
    app.register_blueprint(coordenador_bp, url_prefix='/coordenador')
    app.register_blueprint(instrutor_bp, url_prefix='/instrutor')
    app.register_blueprint(login_bp, url_prefix='/login')

    app.teardown_appcontext(close_db)

    @app.route('/')
    def index():
      
        return redirect(url_for('geral_bp.home'))

    return app