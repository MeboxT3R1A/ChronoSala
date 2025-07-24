# app/routes/coordenador/__init__.py
from flask import Blueprint

coordenador_bp = Blueprint('coordenador_bp', __name__, url_prefix='/coordenador')

# Importa views para registrar rotas
from .views import painel, sala, funcionario, reserva