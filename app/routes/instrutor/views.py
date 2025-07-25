from flask import render_template, request, session, redirect, url_for, flash
from app.routes.instrutor import instrutor_bp as instrutor
from app.decorators import login_required, role_required
from app.routes.instrutor.services.instrutor_services import obter_salas_com_reservas
from app.routes.instrutor.services.reserva_services import processar_reserva, buscar_reservas_por_email, atualizar_status_reserva, buscar_sala_por_id

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
            'responsavel': session.get('email')
        }
        return processar_reserva(dados_reserva)
    
    # GET
    try:
        sala_id = request.args.get('sala_id')
        sala_escolhida = None
        if sala_id:
            # Função para buscar sala pelo ID — ajuste para seu serviço
            sala_escolhida = buscar_sala_por_id(sala_id)  
            if not sala_escolhida:
                return "Sala não encontrada", 404
        
        return render_template('instrutor/reserva_form.html', sala=sala_escolhida)
    except Exception as e:
        print("Erro ao carregar formulário de reserva:", e)
        return f"Erro ao carregar formulário: {e}"


@instrutor.route('/minhas-reservas', methods=['GET'])
@login_required
@role_required(['Instrutor'])
def minhas_reservas():
    try:
        email = session.get('email')
        reservas = buscar_reservas_por_email(email)
        return render_template('instrutor/minhas_reservas.html', reservas=reservas)
    except Exception as e:
        print(f"Erro ao carregar reservas do instrutor: {e}")
        flash("Erro ao carregar suas reservas.", "danger")
        return redirect(url_for('instrutor_bp.painel_instrutor'))
    
@instrutor.route('/cancelar-reserva', methods=['POST'])
@login_required
@role_required(['Instrutor'])
def cancelar_reserva():
    try:
        id_reserva = request.form.get('id_reserva')
        if not id_reserva:
            flash("Reserva inválida.", "danger")
            return redirect(url_for('instrutor_bp.minhas_reservas'))

        atualizar_status_reserva(id_reserva, 'cancelado')
        flash("Reserva cancelada com sucesso!", "success")
    except Exception as e:
        print(f"Erro ao cancelar reserva: {e}")
        flash("Erro ao cancelar a reserva.", "danger")
    return redirect(url_for('instrutor_bp.minhas_reservas'))