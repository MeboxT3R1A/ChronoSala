# app/routes/coordenador/views/funcionario.py
from flask import (
    render_template, request,
    redirect, url_for, flash,
)
from app.db import get_db
from app.routes.coordenador import coordenador_bp as coordenador
import pymysql.err
import pymysql.cursors
from app.decorators import login_required, role_required
from werkzeug.security import generate_password_hash


@coordenador.route('/listar_funcionarios')
@login_required
@role_required(['Coordenador'])
def listar_funcionarios():
    busca = request.args.get('busca')
    filtro_funcao = request.args.get('filtro_funcao')

    try:
        conn = get_db()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = "SELECT * FROM funcionario WHERE 1=1"
            params = []

            if busca:
                query += " AND (nome LIKE %s OR matricula = %s)"
                params.extend((f"%{busca}%", busca))

            if filtro_funcao:
                query += " AND funcao = %s"
                params.append(filtro_funcao)

            cursor.execute(query, params)
            funcionarios = cursor.fetchall()
        return render_template('coordenador/painel_funcionario.html', funcionarios=funcionarios)

    except Exception as e:
        flash(f"Erro ao buscar funcionários: {e}", "danger")
        return render_template('painel_funcionario.html', funcionarios=[])

    
@coordenador.route('/editar_funcionario/<email>', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador'])
def editar_funcionario(email):
    conn = get_db()
    if request.method == 'POST':
        # Pegar dados do formulário
        nome = request.form['nome']
        matricula = request.form['matricula']
        senha = request.form['senha']
        funcao = request.form['funcao']

        try:
            with conn.cursor() as cursor:
                query = """
                    UPDATE funcionario
                    SET nome=%s, matricula=%s, senha=%s, funcao=%s
                    WHERE email=%s
                """
                cursor.execute(query, (nome, matricula, senha, funcao, email))
                conn.commit()
                flash('Funcionário atualizado com sucesso!', 'success')
                return redirect(url_for('coordenador_bp.listar_funcionarios'))
        except pymysql.err.Error as err:
            flash(f'Erro ao atualizar funcionário: {err}', 'danger')
            return redirect(url_for('coordenador_bp.listar_funcionarios'))

    else:
        # Método GET: buscar dados para preencher o formulário
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM funcionario WHERE email=%s", (email,))
            funcionario = cursor.fetchone()
            if funcionario is None:
                flash('Funcionário não encontrado.', 'warning')
                return redirect(url_for('coordenador_bp.listar_funcionarios'))

        return render_template('coordenador/editar_funcionario.html', funcionario=funcionario)