# app/routes/coordenador/views.py
from flask import render_template, request, redirect, url_for, flash, session
from app.db import get_db
from . import coordenador_bp
from app.decorators import login_required, role_required

@coordenador_bp.route('/')
@login_required
@role_required(['Coordenador', 'Administrador'])
def painel_coordenador():
    """
    Rota para o painel do coordenador.
    Exibe a lista de salas.
    """
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            # Seleciona todas as salas, SEM capacidade.
            cursor.execute("SELECT nome_sala, status_sala FROM sala")
            salas = cursor.fetchall()
        return render_template('coordenador.html', salas=salas)

    except Exception as e:
        flash(f'Erro ao acessar salas: {e}', 'error')
        return redirect(url_for('geral_bp.home'))


@coordenador_bp.route('/excluir/<nome_sala>', methods=['POST'])
@login_required
@role_required(['Coordenador', 'Administrador'])
def excluir_sala(nome_sala):
    """
    Rota para excluir uma sala.
    """
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM sala WHERE nome_sala = %s", (nome_sala,))
            conn.commit()
            flash('Sala excluída com sucesso.', 'success')

    except Exception as e:
        flash(f'Erro ao excluir sala: {e}', 'error')

    return redirect(url_for('coordenador_bp.painel_coordenador'))


@coordenador_bp.route('/editar/<nome_sala>', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador', 'Administrador'])
def editar_sala(nome_sala):
    """
    Rota para editar o status de uma sala.
    """
    try:
        conn = get_db()
        with conn.cursor() as cursor:

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