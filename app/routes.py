from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conectar
import pymysql.cursors

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('login.html')

@routes.route('/instrutor')
def painel_instrutor():
    return render_template('instrutor.html')

@routes.route('/coordenador')
def painel_coordenador():
    conexao = None
    cursor = None
    try:
        print("Tentando conectar...")
        conexao = conectar()
        print("Conectado!")
        cursor = conexao.cursor(pymysql.cursors.DictCursor)  # Use DictCursor para dicionários
        cursor.execute("SELECT * FROM sala")
        salas = cursor.fetchall()
        print("Dados recebidos:", salas)
        return render_template('coordenador.html', salas=salas)
    except Exception as e:
        print("Erro ao acessar banco:", e)
        return f"Erro: {e}"
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

@routes.route('/coordenador/excluir/<int:id>', methods=['POST'])
def excluir_sala(id):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM sala WHERE id = %s", (id,))
        conexao.commit()
        flash('Sala excluída com sucesso.')
    except Exception as e:
        flash(f'Erro ao excluir sala: {e}')
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
    return redirect(url_for('routes.painel_coordenador'))

@routes.route('/coordenador/editar/<int:id>', methods=['GET', 'POST'])
def editar_sala(id):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            nome = request.form['nome']
            status = request.form['status']
            imagem = request.form['imagem']
            cursor.execute(
                "UPDATE sala SET nome=%s, status=%s, imagem=%s WHERE id=%s",
                (nome, status, imagem, id)
            )
            conexao.commit()
            flash('Sala atualizada com sucesso.')
            return redirect(url_for('routes.painel_coordenador'))

        cursor.execute("SELECT * FROM sala WHERE id=%s", (id,))
        sala = cursor.fetchone()

        if not sala:
            flash('Sala não encontrada.')
            return redirect(url_for('routes.painel_coordenador'))

        imagens = ['img1.png', 'img2.png', 'img3.png']  # Ajuste conforme seus arquivos reais
        return render_template('editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        flash(f'Erro ao editar sala: {e}')
        return redirect(url_for('routes.painel_coordenador'))
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
