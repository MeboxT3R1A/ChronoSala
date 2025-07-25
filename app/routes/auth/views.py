# app/routes/auth/views.py
from flask import render_template, request, redirect, url_for, flash
from . import login_bp

from app.routes.auth.services.auth_service import autenticar_login
from app.routes.auth.services.session_manager import salvar_sessao, destino_por_funcao

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    usuario_preenchido = ''
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        usuario_preenchido = usuario

        try:
            funcionario = autenticar_login(usuario, senha)
            if funcionario:
                salvar_sessao(funcionario)
                rota = destino_por_funcao(funcionario['funcao'])
                if rota:
                    return redirect(url_for(rota))
                else:
                    flash('Função inválida.', 'danger')
            else:
                flash('Credenciais inválidas.', 'danger')

        except Exception as e:
            flash(f'Erro interno: {e}', 'error')

    return render_template('auth/login.html', usuario_preenchido=usuario_preenchido, hide_sidebar=True)