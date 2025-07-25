# app/decorators.py
from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    """
    Decorador para verificar se o usuário está logado.
    Redireciona para a página de login se não estiver.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica se 'logged_in' está na sessão e é True.
        if 'logged_in' not in session or not session['logged_in']:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'logged_in' not in session or not session['logged_in']:
                flash('Você precisa estar logado para acessar esta página.', 'warning')
                return redirect(url_for('login_bp.login'))
            
            if session.get('user_role') not in allowed_roles:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                # Redireciona para uma página adequada baseada no papel do usuário
                if session.get('user_role') == 'Coordenador':
                    return redirect(url_for('coordenador_bp.painel_coordenador'))
                elif session.get('user_role') in ['Instrutor', 'Administrador']:
                    return redirect(url_for('instrutor_bp.painel_instrutor'))
                else:
                    return redirect(url_for('geral_bp.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator