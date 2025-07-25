from flask import render_template, request, session
from app.routes.instrutor import instrutor_bp as instrutor
from app.decorators import login_required, role_required
from app.routes.instrutor.services.instrutor_services import obter_salas_com_reservas
from app.routes.instrutor.services.reserva_services import processar_reserva

@instrutor.route('')
@login_required
@role_required(['Instrutor', 'Administrador'])
def painel_instrutor():
    try:
        salas = obter_salas_com_reservas()
        return render_template('instrutor/painel_instrutor.html', salas=salas)
    except Exception as e:
        print("Erro ao carregar painel do instrutor:", e)
        return f"Erro: {e}"

@instrutor.route('/reservar', methods=['GET', 'POST'])
@login_required
@role_required(['Instrutor', 'Administrador'])
def criar_reserva():
    if request.method == 'POST':
        dados_reserva = {
            'nome_sala': request.form['nome_sala'],
            'data_reserva': request.form['data_reserva'],
            'hora_inicio': request.form['hora_inicio'],
            'hora_fim': request.form['hora_fim'],
            'responsavel': request.form['responsavel']
        }
        return processar_reserva(dados_reserva)
    
    # GET
    try:
        salas = obter_salas_com_reservas()
        return render_template('instrutor/reserva_form.html', salas=salas)
    except Exception as e:
        print("Erro ao carregar formulário de reserva:", e)
        return f"Erro ao carregar formulário: {e}"
