from flask import render_template, request, redirect, url_for, flash, session
from app.db import get_db
from app.routes.instrutor import instrutor_bp
from app.decorators import login_required, role_required
from datetime import time, timedelta, datetime

def timedelta_to_time(td):
    total_seconds = int(td.total_seconds())
    horas = total_seconds // 3600
    minutos = (total_seconds % 3600) // 60
    segundos = total_seconds % 60
    return time(horas, minutos, segundos)

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

                query_conflito = """
                    SELECT * FROM reserva 
                    WHERE id_sala = %s AND data_res = %s
                    AND (%s < termino AND %s > inicio)
                """
                cursor.execute(query_conflito, (sala_id, data_res, hora_fim, hora_inicio))
                conflito = cursor.fetchone()

                if conflito:
                    flash("Já existe uma reserva nesse horário para essa sala.", "warning")
                    return redirect(url_for('instrutor_bp.formulario_reserva', sala_id=sala_id))

                cursor.execute("""
                    INSERT INTO reserva (id_sala, email, inicio, termino, data_res)
                    VALUES (%s, %s, %s, %s, %s)
                """, (sala_id, email_usuario, hora_inicio, hora_fim, data_res))
                conn.commit()

                flash('Reserva criada com sucesso!', 'success')
                return redirect(url_for('instrutor_bp.painel_instrutor'))

            return render_template('instrutor/reserva_form.html', sala_id=sala_id, nome_sala=sala['nome_sala'])

    except Exception as e:
        print("Erro ao criar reserva:", e)
        flash("Erro ao processar reserva.", "danger")
        return redirect(url_for('instrutor_bp.painel_instrutor'))

@instrutor_bp.route('/minhas_reservas')
@login_required
@role_required(['Instrutor', 'Administrador'])
def minhas_reservas():
    conn = get_db()
    try:
        email_usuario = session.get('email')
        if not email_usuario:
            flash("Sessão expirada ou inválida. Faça login novamente.", "danger")
            return redirect(url_for('login_bp.login'))

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT r.id_res, s.nome_sala, r.data_res, r.inicio, r.termino, r.status_res, r.status_chave
                FROM reserva r
                JOIN sala s ON r.id_sala = s.id_sala
                WHERE r.email = %s
                ORDER BY r.data_res DESC, r.inicio ASC
            """, (email_usuario,))
            reservas = cursor.fetchall()

        for reserva in reservas:
            if isinstance(reserva['inicio'], timedelta):
                reserva['inicio'] = timedelta_to_time(reserva['inicio'])
            if isinstance(reserva['termino'], timedelta):
                reserva['termino'] = timedelta_to_time(reserva['termino'])
            if isinstance(reserva['data_res'], str):
                reserva['data_res'] = datetime.strptime(reserva['data_res'], '%Y-%m-%d').date()

        return render_template('instrutor/minhas_reservas.html', reservas=reservas)

    except Exception as e:
        print("Erro ao buscar reservas do usuário:", e)
        flash("Erro ao carregar reservas.", "danger")
        return redirect(url_for('instrutor_bp.painel_instrutor'))

@instrutor_bp.route('/cancelar_reserva', methods=['POST'])
@login_required
@role_required(['Instrutor', 'Administrador'])
def cancelar_reserva():
    id_reserva = request.form.get('id_reserva')
    motivo = request.form.get('motivo')
    
    if not motivo:
        flash('Motivo do cancelamento é obrigatório.', 'error')
        return redirect(url_for('instrutor_bp.minhas_reservas'))

    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE reserva
                SET status_res = 'Cancelado', motivo_cancelamento = %s
                WHERE id_res = %s
            """, (motivo, id_reserva))
            db.commit()
            flash('Reserva cancelada com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao cancelar reserva: {str(e)}', 'danger')

    return redirect(url_for('instrutor_bp.minhas_reservas'))