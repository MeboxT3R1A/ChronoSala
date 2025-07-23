from flask import render_template, request, redirect, url_for, flash, session
from app.db import get_db
from app.routes.instrutor import instrutor_bp
from app.decorators import login_required, role_required
from datetime import datetime
import pymysql.cursors

@instrutor_bp.route('/')
@login_required
@role_required(['Instrutor', 'Administrador'])
def painel_instrutor():
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM sala")
            salas = cursor.fetchall()
        return render_template('instrutor/instrutor.html', salas=salas)
    except Exception as e:
        print("Erro ao carregar painel do instrutor:", e)
        return f"Erro: {e}"

@instrutor_bp.route('/reserva/<int:sala_id>', methods=['GET', 'POST'])
@login_required
@role_required(['Instrutor', 'Administrador'])
def formulario_reserva(sala_id):
    try:
        conn = get_db()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT nome_sala FROM sala WHERE id_sala = %s", (sala_id,))
            sala = cursor.fetchone()

            if not sala:
                flash("Sala não encontrada.", "error")
                return redirect(url_for('instrutor_bp.painel_instrutor'))

            # Passa o nome da sala para o template para mostrar no formulário
            return render_template('instrutor/reserva_form.html', sala_id=sala_id, nome_sala=sala['nome_sala'])

    except Exception as e:
        print("Erro ao carregar formulário de reserva:", e)
        flash("Erro interno ao carregar o formulário.", "error")
        return redirect(url_for('instrutor_bp.painel_instrutor'))

@instrutor_bp.route('/nova_reserva/<int:sala_id>', methods=['GET', 'POST'])
@login_required
@role_required(['Instrutor', 'Administrador'])
def nova_reserva(sala_id):
    conn = get_db()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT nome_sala FROM sala WHERE id_sala = %s", (sala_id,))
            sala = cursor.fetchone()

            if not sala:
                flash("Sala não encontrada.", "error")
                return redirect(url_for('instrutor_bp.painel_instrutor'))

            if request.method == 'POST':
                data_res = request.form.get('data_res')
                hora_inicio = request.form.get('hora_inicio')
                hora_fim = request.form.get('hora_fim')
                responsavel = request.form.get('responsavel')
                email_usuario = session.get('email')
                
                print("Email do usuário na sessão:", email_usuario)

                cursor.execute("""
                    INSERT INTO reserva (id_sala, email, inicio, termino, data_res)
                    VALUES (%s, %s, %s, %s, %s)
                """, (sala_id, email_usuario, hora_inicio, hora_fim, data_res))
                conn.commit()

                flash('Reserva criada com sucesso!', 'success')
                return redirect(url_for('instrutor_bp.painel_instrutor'))

            # Se for GET, mostra o formulário com o nome da sala
            return render_template('instrutor/reserva_form.html', sala_id=sala_id, nome_sala=sala['nome_sala'])

    except Exception as e:
        print("Erro ao criar reserva:", e)
        flash("Erro ao processar reserva.", "danger")
        return redirect(url_for('instrutor_bp.painel_instrutor'))
