from flask import Blueprint,render_template, request, redirect, url_for, flash
from app.db import get_db
from app.routes.coordenador import coordenador_bp as coordenador
import pymysql.err
import pymysql.cursors
from datetime import datetime


@coordenador.route('/')
def painel_coordenador():
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:  # <-- Aqui
            cursor.execute("SELECT * FROM sala")
            salas = cursor.fetchall()  # salas será lista de dicts
        return render_template('coordenador.html', salas=salas)

    except Exception as e:
        print("Erro ao acessar banco:", e)
        return f"Erro ao acessar banco de dados: {e}"

@coordenador.route('/editar/<nome_sala>', methods=['GET', 'POST'])
def editar_sala(nome_sala):
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:  # <-- Aqui

            if request.method == 'POST':
                status = request.form['status']
                cursor.execute(
                    "UPDATE sala SET status_sala=%s WHERE nome_sala=%s",
                    (status, nome_sala)
                )
                conn.commit()
                flash('Sala atualizada com sucesso.')
                return redirect(url_for('coordenador.painel_coordenador'))

            cursor.execute("SELECT * FROM sala WHERE nome_sala=%s", (nome_sala,))
            sala = cursor.fetchone()  # sala será dict

            if not sala:
                flash('Sala não encontrada.')
                return redirect(url_for('coordenador.painel_coordenador'))

        imagens = ['img1.png', 'img2.png', 'img3.png']
        return render_template('editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        flash(f'Erro ao editar sala: {e}')
        return redirect(url_for('coordenador.painel_coordenador'))

@coordenador.route('/excluir/<nome_sala>', methods=['POST'])
def excluir_sala(nome_sala):
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:  # <-- Aqui
            cursor.execute("DELETE FROM sala WHERE nome_sala = %s", (nome_sala,))
            conn.commit()
            flash('Sala excluída com sucesso.')

    except Exception as e:
        flash(f'Erro ao excluir sala: {e}')

    return redirect(url_for('coordenador.painel_coordenador'))\

# ✅ CORREÇÃO AQUI:
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
            print("Conectado ao banco com sucesso")
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO funcionario (email, nome, matricula, senha, funcao)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (email, nome, matricula, senha, funcao))
                conn.commit()
                flash('Funcionário cadastrado com sucesso!', 'success')

        except pymysql.err.Error as err:
            print("Erro ao cadastrar:", err)
            flash('Erro ao cadastrar funcionário.', 'danger')

        return redirect(url_for('coordenador_bp.cadastro_usuario'))

    return render_template('cadastro_usuario.html')


from flask import render_template, current_app

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
    
@coordenador.route('/editar_funcionario/<email>', methods=['GET', 'POST'])
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

        return render_template('editar_funcionario.html', funcionario=funcionario)


@coordenador.route('/listar_reservas', methods=['GET', 'POST'])
def listar_reservas():
    try:
        conn = get_db()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Filtros opcionais
            nome_sala = request.form.get('nome_sala')
            data_res = request.form.get('data_res')

            query = "SELECT id_res, nome_sala, email, inicio, termino, data_res, status_res, status_chave FROM reserva"
            filtros = []
            valores = []

            if nome_sala:
                filtros.append("nome_sala = %s")
                valores.append(nome_sala)
            if data_res:
                filtros.append("data_res = %s")
                valores.append(data_res)

            if filtros:
                query += " WHERE " + " AND ".join(filtros)

            query += " ORDER BY data_res DESC, inicio ASC"

            cursor.execute(query, valores)
            reservas = cursor.fetchall()

        return render_template('painel_reserva.html', reservas=reservas)
    except Exception as e:
        flash(f'Erro ao listar reservas: {e}', 'danger')
        return redirect(url_for('coordenador_bp.painel_coordenador'))


# Rota para entregar a chave (acionada pelo botão "Entregar")
@coordenador.route('/entregar_chave/<int:id_res>', methods=['POST'])
def entregar_chave(id_res):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE reserva SET status_chave = 'Chave retirada' WHERE id_res = %s", (id_res,))
        conn.commit()
    flash('Chave marcada como ENTREGUE.', 'success')
    return redirect(url_for('coordenador_bp.listar_reservas'))

# Rota para devolver a chave
@coordenador.route('/devolver_chave/<int:id_res>', methods=['POST'])
def devolver_chave(id_res):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE reserva SET status_chave = 'Chave devolvida' WHERE id_res = %s", (id_res,))
        conn.commit()
    flash('Chave marcada como DEVOLVIDA.', 'info')
    return redirect(url_for('coordenador_bp.listar_reservas'))


@coordenador.route('/reservas/criar', methods=['GET', 'POST'])
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

    return render_template('criar_reserva.html', salas=salas)


@coordenador.route('/cancelar_reserva/<int:id_res>', methods=['POST'])
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
