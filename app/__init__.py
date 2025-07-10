from flask import Flask
from app.routes import routes  # import do blueprint

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'chave_secreta_qualquer'

    app.register_blueprint(routes)

    return app
