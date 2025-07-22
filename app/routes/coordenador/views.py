# app/routes/coordenador/views.py
from flask import render_template, request, redirect, url_for, flash, session
from app.db import get_db
from app.routes.coordenador import coordenador_bp as coordenador
import pymysql.err
import pymysql.cursors
from app.decorators import login_required, role_required

@coordenador.route('/')
@login_required
@role_required(['Coordenador', 'Administrador'])
def painel_coordenador():
    """
    Rota para o painel do coordenador.
    Exibe a lista de salas.
    """
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM sala")
            salas = cursor.fetchall()
        return render_template('coordenador.html', salas=salas)

    except Exception as e:
        flash(f'Erro ao acessar salas: {e}', 'error')
        return redirect(url_for('geral_bp.home'))


@coordenador.route('/excluir/<nome_sala>', methods=['POST'])
@login_required
@role_required(['Coordenador', 'Administrador'])
def excluir_sala(nome_sala):
    """
    Rota para excluir uma sala.
    """
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute("DELETE FROM sala WHERE nome_sala = %s", (nome_sala,))
            conn.commit()
            flash('Sala excluída com sucesso.', 'success')

    except Exception as e:
        flash(f'Erro ao excluir sala: {e}', 'error')

    return redirect(url_for('coordenador_bp.painel_coordenador'))


@coordenador.route('/editar/<nome_sala>', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador', 'Administrador'])
def editar_sala(nome_sala):
    """
    Rota para editar o status de uma sala.
    """
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            if request.method == 'POST':
                # Pega o novo status do formulário, SEM capacidade.
                status = request.form['status']

                # Atualiza o status da sala no banco de dados, SEM capacidade.
                cursor.execute(
                    "UPDATE sala SET status_sala=%s WHERE nome_sala=%s",
                    (status, nome_sala)
                )
                conn.commit()
                flash('Sala atualizada com sucesso.', 'success')
                return redirect(url_for('coordenador_bp.painel_coordenador'))

            # Se a requisição é GET, busca os dados da sala para exibir no formulário.
            cursor.execute("SELECT * FROM sala WHERE nome_sala=%s", (nome_sala,))
            sala = cursor.fetchone()

            if not sala:
                flash('Sala não encontrada.', 'warning')
                return redirect(url_for('coordenador_bp.painel_coordenador'))

        imagens = ['img1.png', 'img2.png', 'img3.png']
        return render_template('editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        flash(f'Erro ao editar sala: {e}', 'error')
        return redirect(url_for('coordenador_bp.painel_coordenador'))
    
@coordenador.route('/excluir/<nome_sala>', methods=['POST'])
def excluir_sala(nome_sala):
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute("DELETE FROM sala WHERE nome_sala = %s", (nome_sala,))
            conn.commit()
            flash('Sala excluída com sucesso.')
    except Exception as e:
        flash(f'Erro ao excluir sala: {e}')

    return redirect(url_for('coordenador.painel_coordenador'))

@coordenador.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        matricula = request.form['matricula']
        senha = request.form['senha']
        funcao = request.form['funcao']

        try:
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO funcionario (email, nome, matricula, senha, funcao)
                    VALUES (%s, %s, %s, %s, %s)
                """, (email, nome, matricula, senha, funcao))
                conn.commit()
                flash('Funcionário cadastrado com sucesso!', 'success')
        except pymysql.err.Error as err:
            print("Erro ao cadastrar:", err)
            flash('Erro ao cadastrar funcionário.', 'danger')

        return redirect(url_for('coordenador.cadastro_usuario'))

    return render_template('cadastro_usuario.html')

@coordenador.route('/listar_funcionarios')
def listar_funcionarios():
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM funcionario;")
            funcionarios = cursor.fetchall()
        return render_template('painel_funcionario.html', funcionarios=funcionarios)
    except Exception as e:
        return f"Erro ao buscar funcionários: {e}"
