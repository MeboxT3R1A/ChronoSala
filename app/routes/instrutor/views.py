# app/routes/instrutor/views.py
from flask import render_template, request, redirect, url_for, flash, session
from app.db import get_db
from . import instrutor_bp
from app.decorators import login_required, role_required

@instrutor_bp.route('/')
@login_required
@role_required(['Instrutor', 'Administrador'])
def painel_instrutor():
    """
    Rota para o painel do instrutor.
    """
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            # Consulta salas disponíveis, SEM capacidade.
            cursor.execute("SELECT nome_sala, status_sala FROM sala WHERE status_sala = 'disponivel'")
            salas_disponiveis = cursor.fetchall()
        return render_template('instrutor.html', salas_disponiveis=salas_disponiveis)
    except Exception as e:
        flash(f'Erro ao carregar salas: {e}', 'error')
        return redirect(url_for('geral_bp.home'))