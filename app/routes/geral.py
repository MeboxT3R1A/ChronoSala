from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conectar

geral = Blueprint('geral', __name__)

@geral.route('/')
def home():
    return render_template('loginTeste.html')