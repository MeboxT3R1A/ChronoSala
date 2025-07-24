# app/routes/coordenador/views/funcionario.py

from flask import render_template, request, redirect, url_for, flash
from app.routes.coordenador import coordenador_bp as coordenador
from app.decorators import login_required, role_required
from app.routes.coordenador.services.funcionario_service import (
    buscar_funcionarios,
    buscar_funcionario_por_email,
    atualizar_funcionario,
)
from pymysql.err import Error


@coordenador.route('/listar_funcionarios')
@login_required
@role_required(['Coordenador'])
def listar_funcionarios():
    busca = request.args.get('busca')
    filtro_funcao = request.args.get('filtro_funcao')

    try:
        funcionarios = buscar_funcionarios(busca, filtro_funcao)
        return render_template('coordenador/painel_funcionario.html', funcionarios=funcionarios)

    except Exception as e:
        flash(f"Erro ao buscar funcionários: {e}", "danger")
        return render_template('coordenador/painel_funcionario.html', funcionarios=[])


@coordenador.route('/editar_funcionario/<email>', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador'])
def editar_funcionario(email):
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        senha = request.form['senha']
        funcao = request.form['funcao']

        try:
            atualizar_funcionario(email, nome, matricula, senha, funcao)
            flash('Funcionário atualizado com sucesso!', 'success')
        except Error as err:
            flash(f'Erro ao atualizar funcionário: {err}', 'danger')

        return redirect(url_for('coordenador_bp.listar_funcionarios'))

    funcionario = buscar_funcionario_por_email(email)
    if not funcionario:
        flash('Funcionário não encontrado.', 'warning')
        return redirect(url_for('coordenador_bp.listar_funcionarios'))

    return render_template('coordenador/editar_funcionario.html', funcionario=funcionario)
