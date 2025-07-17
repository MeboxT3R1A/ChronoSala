# app/__init__.py
from flask import Flask, render_template
import os
from config import DevelopmentConfig, ProductionConfig
from flask_migrate import Migrate

from app.db import db # CORREÇÃO: Importe a instância 'db' de dentro do pacote 'app'

# Importe seus modelos para que o SQLAlchemy e Flask-Migrate os conheçam
from app.models import models # OU from app.models.models import Funcionario, Sala, ...

# Crie a instância do Flask-Migrate NO ESCOPO GLOBAL
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db) # Inicializa o Flask-Migrate

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.coordenador import coordenador_bp
    from app.routes.instrutor import instrutor_bp
    # É CRUCIAL que app/routes/geral.py seja convertido em um Blueprint!
    # Por exemplo, crie uma pasta 'app/routes/geral/' com '__init__.py' e 'views.py' dentro.
    # E em 'app/routes/geral/__init__.py', defina 'geral_bp = Blueprint(...)'.
    from app.routes.geral import geral_bp # Assumindo que você converteu geral.py para um Blueprint

    app.register_blueprint(geral_bp)
    app.register_blueprint(coordenador_bp, url_prefix='/coordenador')
    app.register_blueprint(instrutor_bp, url_prefix='/instrutor')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app