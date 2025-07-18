from flask import render_template, request, jsonify
from app.db import get_db
from app.routes.instrutor import instrutor_bp as instrutor
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
                cursor.execute("SELECT * FROM reserva WHERE nome_sala = %s", (sala['nome_sala'],))
                sala['reservas'] = cursor.fetchall()

        return render_template('instrutor.html', salas=salas)

    except Exception as e:
        print("Erro ao carregar painel do instrutor:", e)
        return f"Erro: {e}"

@instrutor.route('/reservar', methods=['POST'])
def criar_reserva():
    try:
        nome_sala = request.form['nome_sala']
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
            # Verifica conflito
            cursor.execute("""
                SELECT * FROM reserva 
                WHERE nome_sala = %s AND data_reserva = %s AND (
                    (hora_inicio <= %s AND hora_fim > %s) OR
                    (hora_inicio < %s AND hora_fim >= %s) OR
                    (hora_inicio >= %s AND hora_fim <= %s)
                )
            """, (nome_sala, data_reserva, hora_inicio, hora_inicio, hora_fim, hora_fim, hora_inicio, hora_fim))

            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Conflito com outra reserva!'})

            # Cria reserva
            cursor.execute("""
                INSERT INTO reserva (nome_sala, data_reserva, hora_inicio, hora_fim, responsavel)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome_sala, data_reserva, hora_inicio, hora_fim, responsavel))

            # Atualiza status da sala
            cursor.execute("UPDATE sala SET status_sala = 'ocupada' WHERE nome_sala = %s", (nome_sala,))
            conn.commit()

        return jsonify({'success': True, 'message': 'Reserva criada com sucesso!'})

    except Exception as e:
        import traceback
        print("Erro na reserva:\n", traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })
