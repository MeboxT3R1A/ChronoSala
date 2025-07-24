# app/routes/coordenador/__init__.py
from flask import Blueprint

coordenador_bp = Blueprint('coordenador_bp', __name__, url_prefix='/coordenador')

# Importa views (rotas) para registrar no blueprint
from .views import painel, sala, funcionario, reserva
