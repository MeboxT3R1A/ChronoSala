from flask import Blueprint

instrutor_bp = Blueprint(
    "instrutor_bp", 
    __name__, 
    url_prefix='/instrutor',
    template_folder='../../../templates/instrutor'
)

# Import views after blueprint creation to avoid circular imports
from . import views