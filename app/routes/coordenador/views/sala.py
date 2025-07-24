# app/routes/coordenador/views/sala.py
from flask import (
    render_template, request,
    redirect, url_for, flash,
)
from app.db import get_db
from app.routes.coordenador import coordenador_bp as coordenador
import pymysql.cursors
from app.decorators import login_required, role_required

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

@coordenador.route('/adicionar_sala', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def adicionar_sala():
    """Rota para adicionar nova sala"""
    try:
        nome_sala = request.form['nome_sala']
        status_sala = request.form['status_sala']
        
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO sala (nome_sala, status_sala) VALUES (%s, %s)",
                (nome_sala, status_sala)
            )
            conn.commit()
            flash('Sala adicionada com sucesso!', 'success')
    except pymysql.err.IntegrityError:
        flash('Esta sala já existe!', 'error')
    except Exception as e:
        flash(f'Erro ao adicionar sala: {str(e)}', 'error')
    
    return redirect(url_for('coordenador_bp.painel_coordenador'))   
