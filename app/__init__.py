from flask import Flask, render_template
from app.db import close_db  # importa função para fechar

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # Importa e registra os blueprints
    from app.routes.coordenador import coordenador_bp
    from app.routes.instrutor import instrutor_bp
    from app.routes.geral import geral_bp
    from app.routes.auth import login_bp

    app.register_blueprint(geral_bp)
    app.register_blueprint(coordenador_bp, url_prefix='/coordenador')
    app.register_blueprint(instrutor_bp, url_prefix='/instrutor')
    app.register_blueprint(login_bp, url_prefix='/login')

    # Fecha conexão no final da requisição
    app.teardown_appcontext(close_db)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
