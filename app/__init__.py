from flask import Flask
from app.routes.coordenador import coordenador
from app.routes.instrutor import instrutor
from app.routes.geral import geral
from app.db import conectar
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def liberar_salas_expiradas():
    try:
        now = datetime.now().time()
        hoje = datetime.now().date()

        with conectar() as conexao:
            with conexao.cursor() as cursor:
                # Seleciona salas com reservas finalizadas
                cursor.execute("""
                    SELECT sala_id FROM reservas
                    WHERE data_reserva = %s AND hora_fim <= %s
                """, (hoje, now))

                salas_para_liberar = cursor.fetchall()

                for row in salas_para_liberar:
                    sala_id = row[0]
                    # Atualiza status da sala
                    cursor.execute("UPDATE sala SET status = 'disponivel' WHERE id = %s", (sala_id,))
                
                # Apaga todas as reservas finalizadas
                cursor.execute("""
                    DELETE FROM reservas
                    WHERE data_reserva = %s AND hora_fim <= %s
                """, (hoje, now))
            
            conexao.commit()

    except Exception as e:
        print("[SCHEDULER ERRO]:", e)

def create_app():
    app = Flask(__name__)
    app.secret_key = '1234567890abcdef'

    # Registra rotas
    app.register_blueprint(geral)
    app.register_blueprint(coordenador, url_prefix='/coordenador')
    app.register_blueprint(instrutor, url_prefix='/instrutor')

    # Inicia scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(liberar_salas_expiradas, 'interval', seconds=60)
    scheduler.start()

    return app
