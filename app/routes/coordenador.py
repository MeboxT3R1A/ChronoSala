from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conectar
import mysql.connector


coordenador = Blueprint('coordenador', __name__)

@coordenador.route('/')
def painel_coordenador():
    try:
        print("Tentando conectar...")
        with conectar() as conexao:
            with conexao.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM sala")
                salas = cursor.fetchall()
                print("Dados recebidos:", salas)
        return render_template('coordenador.html', salas=salas)

    except Exception as e:
        print("Erro ao acessar banco:", e)
        return f"Erro ao acessar banco de dados: {e}"

@coordenador.route('/excluir/<int:id>', methods=['POST'])
def excluir_sala(id):
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("DELETE FROM sala WHERE id = %s", (id,))
                conexao.commit()
                flash('Sala excluída com sucesso.')

    except Exception as e:
        flash(f'Erro ao excluir sala: {e}')

    return redirect(url_for('coordenador.painel_coordenador'))

@coordenador.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_sala(id):
    try:
        with conectar() as conexao:
            with conexao.cursor(dictionary=True) as cursor:

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
                    return redirect(url_for('coordenador.painel_coordenador'))

                cursor.execute("SELECT * FROM sala WHERE id=%s", (id,))
                sala = cursor.fetchone()

                if not sala:
                    flash('Sala não encontrada.')
                    return redirect(url_for('coordenador.painel_coordenador'))

        imagens = ['img1.png', 'img2.png', 'img3.png']  # Atualize com imagens reais
        return render_template('editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        flash(f'Erro ao editar sala: {e}')
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
            conn = conectar()  # Use sua função personalizada aqui
            cursor = conn.cursor()

            query = """
                INSERT INTO funcionarios (email, nome, matricula, senha, funcao)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (email, nome, matricula, senha, funcao))
            conn.commit()
            flash('Funcionário cadastrado com sucesso!', 'success')

        except mysql.connector.Error as err:
            print("Erro ao cadastrar:", err)
            flash('Erro ao cadastrar funcionário.', 'danger')

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('coordenador.cadastro_usuario'))

    return render_template('cadastro_usuario.html')