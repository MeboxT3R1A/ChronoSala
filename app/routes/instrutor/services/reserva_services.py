from flask import flash, redirect, url_for
from datetime import datetime
from app.db import get_db
import pymysql.cursors

def processar_reserva(dados):
    try:
        nome_sala = dados['nome_sala']
        data_reserva = dados['data_reserva']
        hora_inicio = dados['hora_inicio']
        hora_fim = dados['hora_fim']
        responsavel = dados['responsavel']

        data = datetime.strptime(data_reserva, '%d/%m/%Y').date()
        inicio = datetime.strptime(hora_inicio, '%H:%M').time()
        fim = datetime.strptime(hora_fim, '%H:%M').time()

        if fim <= inicio:
            flash('Hora final deve ser após a inicial', 'error')
            return redirect(url_for('instrutor_bp.exibir_form_reserva'))

        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:

            cursor.execute("SELECT id_sala FROM sala WHERE nome_sala = %s", (nome_sala,))
            sala = cursor.fetchone()
            if not sala:
                flash('Sala não encontrada!', 'error')
                return redirect(url_for('instrutor_bp.exibir_form_reserva'))

            id_sala = sala['id_sala']

            cursor.execute("""
                SELECT * FROM reserva 
                WHERE id_sala = %s AND data_res = %s AND (
                    (inicio <= %s AND termino > %s) OR
                    (inicio < %s AND termino >= %s) OR
                    (inicio >= %s AND termino <= %s)
                )
            """, (id_sala, data, inicio, inicio, fim, fim, inicio, fim))

            if cursor.fetchone():
                flash('Conflito com outra reserva!', 'error')
                return redirect(url_for('instrutor_bp.exibir_form_reserva'))

            cursor.execute("""
                INSERT INTO reserva (id_sala, data_res, inicio, termino, email)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_sala, data, inicio, fim, responsavel))

            cursor.execute("UPDATE sala SET status_sala = 'reservado' WHERE id_sala = %s", (id_sala,))
            conn.commit()

        flash('Reserva criada com sucesso!', 'success')
        return redirect(url_for('instrutor_bp.painel_instrutor'))

    except Exception as e:
        import traceback
        print("Erro na lógica de reserva:\n", traceback.format_exc())
        flash(f'Erro interno: {str(e)}', 'error')
        return redirect(url_for('instrutor_bp.exibir_form_reserva'))
