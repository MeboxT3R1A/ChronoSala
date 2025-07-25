# app/routes/instrutor/__init__.py
from flask import Blueprint
instrutor_bp = Blueprint("instrutor_bp", __name__, url_prefix="/instrutor")
from . import views