from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conectar

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('login.html')

@routes.route('/instrutor')
def painel_instrutor():
    return render_template('instrutor.html')

@routes.route('/coordenador')
def painel_coordenador():
    try:
        print("Tentando conectar...")
        conexao = conectar()
        print("Conectado!")
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sala")
        salas = cursor.fetchall()
        print("Dados recebidos:", salas)
        cursor.close()
        conexao.close()
        return "OK"
    except Exception as e:
        print("Erro ao acessar banco:", e)
        return f"Erro: {e}"


@routes.route('/coordenador/excluir/<int:id>', methods=['POST'])
def excluir_sala(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM sala WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    flash('Sala excluída com sucesso.')
    return redirect(url_for('routes.painel_coordenador'))

@routes.route('/coordenador/editar/<int:id>', methods=['GET', 'POST'])
def editar_sala(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    if request.method == 'POST':
        nome = request.form['nome']
        status = request.form['status']
        imagem = request.form['imagem']
        cursor.execute("UPDATE sala SET nome=%s, status=%s, imagem=%s WHERE id=%s", (nome, status, imagem, id))
        conexao.commit()
        cursor.close()
        conexao.close()
        flash('Sala atualizada com sucesso.')
        return redirect(url_for('routes.painel_coordenador'))

    cursor.execute("SELECT * FROM sala WHERE id=%s", (id,))
    sala = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not sala:
        flash('Sala não encontrada.')
        return redirect(url_for('routes.painel_coordenador'))

    # Aqui você deve fornecer a lista de imagens para o select da edição
    imagens = ['img1.png', 'img2.png', 'img3.png']  # ajuste conforme seus arquivos reais

    return render_template('editar_sala.html', sala=sala, imagens=imagens)