# app/routes/geral.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

geral_bp = Blueprint('geral_bp', __name__)

@geral_bp.route('/')
def home():

    if 'logged_in' in session and session['logged_in']:
        role = session.get('user_role')
        if role == 'Coordenador':
            return redirect(url_for('coordenador_bp.painel_coordenador'))
        elif role == 'Instrutor' or role == 'Administrador':
            return redirect(url_for('instrutor_bp.painel_instrutor'))

    return render_template('auth/login.html')

@geral_bp.route('/logout')
def logout():

    session.clear() # Limpa todas as variáveis da sessão.
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('geral_bp.home'))