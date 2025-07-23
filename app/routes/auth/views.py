# app/routes/auth/views.py
from flask import render_template, request, redirect, url_for, flash, session
from . import login_bp

from auth.services.auth_service import buscar_funcionario_por_usuario, verificar_senha
from auth.services.session_manager import salvar_sessao, destino_por_funcao

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    print("== LOGIN EXECUTADO ==")

    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        usuario_preenchido = usuario

        try:
            funcionario = buscar_funcionario_por_usuario(usuario)

            if funcionario and verificar_senha(senha, funcionario['senha']):
                salvar_sessao(funcionario)
                rota = destino_por_funcao(funcionario['funcao'])

                if rota:
                    return redirect(url_for(rota))
                else:
                    flash('Função de usuário não reconhecida.', 'danger')
                    return redirect(url_for('login_bp.login'))
            else:
                flash('Credenciais inválidas.', 'danger')
                return redirect(url_for('login_bp.login'))

        except Exception as e:
            flash(f'Erro interno: {e}', 'error')
            return render_template('auth/login.html', usuario_preenchido=usuario_preenchido)

    return render_template('auth/login.html', usuario_preenchido='', hide_sidebar=True)
