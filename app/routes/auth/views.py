# app/routes/auth/views.py
from flask import render_template, request, redirect, url_for, flash, session
from app.db import get_db
from . import login_bp
from werkzeug.security import check_password_hash
import pymysql.cursors

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    print("== LOGIN EXECUTADO ==")

    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        usuario_preenchido = usuario

        try:
            db = get_db()
            cursor = db.cursor(pymysql.cursors.DictCursor)

            query = "SELECT email, nome, funcao, senha FROM funcionario WHERE email = %s OR matricula = %s"
            cursor.execute(query, (usuario, usuario))
            funcionario = cursor.fetchone()

            if funcionario and check_password_hash(funcionario['senha'], senha):
                session['logged_in'] = True
                session['user_role'] = funcionario['funcao']
                session['user_name'] = funcionario['nome']
                print('== ROLE SALVA NA SESSÃO:', session['user_role'])
                
                destinos = {
                    'Coordenador': 'coordenador_bp.painel_coordenador',
                    'Instrutor': 'instrutor_bp.painel_instrutor',
                }
                rota = destinos.get(funcionario['funcao'])


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

    return render_template('auth/login.html', usuario_preenchido='')
