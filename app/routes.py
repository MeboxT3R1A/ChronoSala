from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/coordenador')
def painel_coordenador():
    return render_template('coordenador.html')

@routes.route('/instrutor')
def painel_instrutor():
    return render_template('instrutor.html')