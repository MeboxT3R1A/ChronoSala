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
    """
    Decorador para verificar se o usuário logado tem uma das funções permitidas.
    Aceita uma lista de funções permitidas.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Primeiro, verifica se o usuário está logado.
            if 'logged_in' not in session or not session['logged_in']:
                flash('Você precisa estar logado para acessar esta página.', 'warning')
                return redirect(url_for('login_bp.login'))
            
            # Verifica se a função do usuário está na lista de funções permitidas.
            print('DEBUG - allowed_roles:', allowed_roles)
            print('DEBUG - user_role:', session.get('user_role'))
            print('DEBUG - repr(user_role):', repr(session.get('user_role')))

            if session.get('user_role') not in allowed_roles:
                print(f"ACESSO NEGADO: {session.get('user_role')} não está em {allowed_roles}")
                flash('Você não tem permissão para acessar esta página.', 'danger')

                # Redireciona para uma página que *não* faz outro redirect automático
                return redirect(url_for('login_bp.login'))  # TEMPORÁRIO para quebrar o loop # Redireciona para uma página genérica ou de erro
            return f(*args, **kwargs)
        return decorated_function
    return decorator