from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from app.routes.coordenador import coordenador_bp as coordenador
import pymysql.err
import pymysql.cursors


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
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO funcionarios (email, nome, matricula, senha, funcao)
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
