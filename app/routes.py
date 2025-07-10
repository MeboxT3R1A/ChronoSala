from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return "<h1>Rota inicial funcionando!</h1>"

