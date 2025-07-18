from flask import render_template, request, redirect, url_for, flash, jsonify
from app.db import get_db
from . import instrutor_bp as instrutor
import pymysql.cursors
from datetime import datetime

@instrutor.route('/')
def painel_instrutor():
    try:
        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM sala")
            salas = cursor.fetchall()

            for sala in salas:
                cursor.execute("SELECT * FROM reservas WHERE sala_id = %s", (sala['id'],))
                sala['reservas'] = cursor.fetchall()

        return render_template('instrutor.html', salas=salas)

    except Exception as e:
        print("Erro ao carregar painel do instrutor:", e)
        return f"Erro: {e}"

@instrutor.route('/reservar', methods=['POST'])
def criar_reserva():
    try:
        sala_id = request.form['sala_id']
        data_reserva = request.form['data_reserva']
        hora_inicio = request.form['hora_inicio']
        hora_fim = request.form['hora_fim']
        responsavel = request.form['responsavel']

        data = datetime.strptime(data_reserva, '%Y-%m-%d').date()
        inicio = datetime.strptime(hora_inicio, '%H:%M').time()
        fim = datetime.strptime(hora_fim, '%H:%M').time()

        if fim <= inicio:
            return jsonify({'success': False, 'message': 'Hora final deve ser após a inicial'})

        conn = get_db()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            # Verifica conflito de horário
            cursor.execute("""
                SELECT * FROM reservas 
                WHERE sala_id = %s AND data_reserva = %s AND (
                    (hora_inicio <= %s AND hora_fim > %s) OR
                    (hora_inicio < %s AND hora_fim >= %s) OR
                    (hora_inicio >= %s AND hora_fim <= %s)
                )
            """, (sala_id, data_reserva, hora_inicio, hora_inicio, hora_fim, hora_fim, hora_inicio, hora_fim))

            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Conflito com outra reserva!'})

            # Cria reserva
            cursor.execute("""
                INSERT INTO reservas (sala_id, data_reserva, hora_inicio, hora_fim, responsavel)
                VALUES (%s, %s, %s, %s, %s)
            """, (sala_id, data_reserva, hora_inicio, hora_fim, responsavel))

            # Atualiza status da sala
            status_valido = 'ocupada'  # compatível com ENUM

            print(f"[DEBUG] Atualizando status da sala {sala_id} para '{status_valido}'")

            sala_id_int = int(sala_id)
            cursor.execute("UPDATE sala SET status = %s WHERE id = %s", (status_valido, sala_id_int))

            conn.commit()

        return jsonify({'success': True, 'message': 'Reserva criada com sucesso!'})

    except Exception as e:
        import traceback
        erro_completo = traceback.format_exc()
        print("Erro na reserva:\n", erro_completo)
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })
