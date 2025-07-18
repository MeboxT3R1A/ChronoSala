from flask import Blueprint

instrutor_bp = Blueprint("instrutor_bp", __name__)

from . import views