from flask import Blueprint, render_template, request, redirect, url_for, flash

geral_bp = Blueprint('geral_bp', __name__)

@geral_bp.route('/')
def home():
    return render_template('loginTeste.html')
