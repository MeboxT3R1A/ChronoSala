# app/__init__.py
from flask import Flask, redirect, url_for
from app.db import close_db
from flask import render_template

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # Registra blueprints
    from app.routes.geral import geral_bp
    from app.routes.auth import login_bp
    from app.routes.coordenador import coordenador_bp
    from app.routes.instrutor import instrutor_bp

    app.register_blueprint(geral_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(coordenador_bp)
    app.register_blueprint(instrutor_bp)

    # Handler de erro 403 — DEVE vir após a criação do app
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('erro/403.html'), 403

    # Encerrar conexão com DB ao fim da request
    app.teardown_appcontext(close_db)

    @app.route('/')
    def index():
        return redirect(url_for('geral_bp.home'))

    return app
