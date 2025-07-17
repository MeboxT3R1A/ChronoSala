from flask import  render_template, request, redirect, url_for, flash
from app.models.db import db
from . import instrutor_bp
from datetime import datetime
from flask import jsonify
import traceback

@instrutor_bp.route('/')
def painel_instrutor():
    try:
        with conectar() as conexao:
            with conexao.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM sala")
                salas = cursor.fetchall()

                for sala in salas:
                    cursor.execute("SELECT * FROM reservas WHERE sala_id = %s", (sala['id'],))
                    sala['reservas'] = cursor.fetchall()

        return render_template('instrutor.html', salas=salas)

    except Exception as e:
        print("Erro ao carregar painel do instrutor:", e)
        return f"Erro: {e}"
    
@instrutor_bp.route('/nova-reserva/<int:sala_id>', methods=['GET', 'POST'])
def nova_reserva(sala_id):
    try:
        with conectar() as conexao:
            with conexao.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM sala WHERE id = %s", (sala_id,))
                sala = cursor.fetchone()

                if not sala:
                    return "Sala não encontrada", 404

        if request.method == 'POST':
            data_reserva = request.form['data_reserva']
            hora_inicio = request.form['hora_inicio']
            hora_fim = request.form['hora_fim']
            responsavel = request.form['responsavel']

            with conectar() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO reservas (sala_id, data_reserva, hora_inicio, hora_fim, responsavel)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (sala_id, data_reserva, hora_inicio, hora_fim, responsavel))

                    cursor.execute("UPDATE sala SET status = %s WHERE id = %s", ('ocupada', sala_id))
                    conexao.commit()

            flash('Reserva criada com sucesso!', 'success')
            return redirect(url_for('instrutor.painel_instrutor'))

        return render_template('nova_reserva.html', sala=sala)

    except Exception as e:
        print("Erro ao criar reserva:", e)
        flash('Erro ao processar a reserva', 'error')
        return redirect(url_for('instrutor.painel_instrutor'))
