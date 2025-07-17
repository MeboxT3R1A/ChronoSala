from flask import  render_template, request, redirect, url_for, flash
from app.models.db import conectar
from . import instrutor_bp

@instrutor_bp.route('/')
def painel_instrutor():
    return render_template('instrutor_bp.html')
