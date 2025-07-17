from flask import Blueprint

coordenador_bp = Blueprint("coordenador_bp", __name__)

from . import views