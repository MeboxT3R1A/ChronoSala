# app/routes/coordenador/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_db
from app.routes.coordenador import coordenador_bp as coordenador
import pymysql.err
import pymysql.cursors
from datetime import datetime
from app.decorators import login_required, role_required

@coordenador.route('/')
@login_required
@role_required(['Coordenador'] )
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
        return render_template('coordenador/coordenador.html', salas=salas)

    except Exception as e:
        print('ERRO AO ACESSAR SALAS:', e)
        flash(f'Erro ao acessar salas: {e}', 'error')
        return render_template('erro/erro_generico.html', erro=str(e))


@coordenador.route('/excluir/<nome_sala>', methods=['POST'])
@login_required
@role_required(['Coordenador'])
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
@role_required(['Coordenador'])
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
        return render_template('coordenador/editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        flash(f'Erro ao editar sala: {e}', 'error')
        return redirect(url_for('coordenador_bp.painel_coordenador'))


@coordenador.route('/cadastro_usuario', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador'])
def cadastro_usuario():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        matricula = request.form['matricula']
        senha = request.form['senha']
        funcao = request.form['funcao']

        try:
            conn = get_db()
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
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

    return render_template('coordenador/cadastro_usuario.html')

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


def buscar_salas():
    conn = get_db()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT nome_sala FROM sala")
        return [row['nome_sala'] for row in cursor.fetchall()]


@coordenador.route('/listar_reservas', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador'])
def listar_reservas():
    try:
        conn = get_db()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            nome_sala = request.args.get('sala')
            data_res = request.args.get('data')
            busca = request.args.get('busca')

            query = "SELECT id_res, nome_sala, email, inicio, termino, data_res, status_res, status_chave FROM reserva"
            filtros = []
            valores = []

            # Filtros existentes
            if nome_sala:
                filtros.append("nome_sala = %s")
                valores.append(nome_sala)
            if data_res:
                filtros.append("data_res = %s")
                valores.append(data_res)

            # Filtro novo para busca geral
            if busca:
                # Verifica se busca é número (id)
                if busca.isdigit():
                    filtros.append("(id_res = %s OR nome_sala LIKE %s OR email LIKE %s)")
                    valores.extend([int(busca), f"%{busca}%", f"%{busca}%"])
                else:
                    filtros.append("(nome_sala LIKE %s OR email LIKE %s)")
                    valores.extend([f"%{busca}%", f"%{busca}%"])

            if filtros:
                query += " WHERE " + " AND ".join(filtros)

            query += " ORDER BY data_res DESC, inicio ASC"

            cursor.execute(query, valores)
            reservas = cursor.fetchall()

        return render_template(
            'coordenador/painel_reserva.html',
            reservas=reservas,
            salas=buscar_salas(),
            sala_selecionada=nome_sala,
            data_selecionada=data_res
        )
    except Exception as e:
        flash(f'Erro ao listar reservas: {e}', 'danger')
        return redirect(url_for('coordenador_bp.painel_coordenador'))

# Rota para entregar a chave (acionada pelo botão "Entregar")
@coordenador.route('/entregar_chave/<int:id_res>', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def entregar_chave(id_res):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE reserva SET status_chave = 'Chave retirada' WHERE id_res = %s", (id_res,))
        conn.commit()
    flash('Chave marcada como ENTREGUE.', 'success')
    return redirect(url_for('coordenador_bp.listar_reservas'))

# Rota para devolver a chave
@coordenador.route('/devolver_chave/<int:id_res>', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def devolver_chave(id_res):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE reserva SET status_chave = 'Chave devolvida' WHERE id_res = %s", (id_res,))
        conn.commit()
    flash('Chave marcada como DEVOLVIDA.', 'info')
    return redirect(url_for('coordenador_bp.listar_reservas'))


@coordenador.route('/reservas/criar', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador'])
def criar_reserva():
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            if request.method == 'POST':
                nome_sala = request.form['nome_sala']
                email = request.form['email']
                data_res = request.form['data_res']
                inicio = request.form['inicio']
                termino = request.form['termino']

                query = """
                    INSERT INTO reserva (nome_sala, email, data_res, inicio, termino, status_res, status_chave)
                    VALUES (%s, %s, %s, %s, %s, 'reservado', 'pendente')
                """
                cursor.execute(query, (nome_sala, email, data_res, inicio, termino))
                conn.commit()

                flash("Reserva criada com sucesso!", "success")
                return redirect(url_for('coordenador.listar_reservas'))

            # GET: buscar salas para dropdown
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT nome_sala FROM sala")
            resultado = cursor.fetchall()
            salas = [row['nome_sala'] for row in resultado]

    except Exception as e:
        flash(f"Erro ao criar reserva: {e}", "danger")
        salas = []

    return render_template('coordenador/criar_reserva.html', salas=salas)


@coordenador.route('/cancelar_reserva/<int:id_res>', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def cancelar_reserva(id_res):
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            # Só cancela se a reserva estiver pendente (chave não entregue)
            cursor.execute(
                "UPDATE reserva SET status_res = 'cancelado' WHERE id_res = %s AND status_chave = 'pendente'",
                (id_res,)
            )
            conn.commit()
        flash('Reserva cancelada com sucesso.', 'warning')
    except Exception as e:
        flash(f'Erro ao cancelar reserva: {e}', 'danger')
    return redirect(url_for('coordenador_bp.listar_reservas'))
