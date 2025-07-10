from flask import Flask
from app.routes import routes  # import do blueprint

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.register_blueprint(routes)
    
    # Configurações adicionais, se houver
    # ex: app.config.from_object('config.ConfigClass')
    
    return app
