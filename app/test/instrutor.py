from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.db import conectar

instrutor = Blueprint('instrutor', __name__)

@instrutor.route('/')
def painel_instrutor():
    return render_template('instrutor.html')
