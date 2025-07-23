# app/routes/instrutor/__init__.py
from flask import Blueprint
instrutor_bp = Blueprint("instrutor_bp", __name__)
from . import views
from datetime import datetime

from datetime import datetime

from datetime import datetime
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # suas configurações, carregamento de Blueprints etc...

    @app.context_processor
    def inject_now():
        return {'now': datetime.now}

    return app
