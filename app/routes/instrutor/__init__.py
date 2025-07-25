# app/routes/instrutor/__init__.py
from flask import Blueprint

instrutor_bp = Blueprint(
    "instrutor_bp",
    __name__,
    template_folder="../../../templates/instrutor",
    static_folder="../../../static"
)

from . import views