# app/routes/coordenador/views/reserva.py

from flask import render_template, request, redirect, url_for, flash
from app.routes.coordenador import coordenador_bp as coordenador
from app.decorators import login_required, role_required
from app.routes.coordenador.services import reserva_service
from app.routes.coordenador.services.coordenador_service import buscar_salas


@coordenador.route('/listar_reservas', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador'])
def listar_reservas():
    try:
        filtros = reserva_service.extrair_filtros_request()
        reservas = reserva_service.buscar_reservas_filtradas(
            nome_sala=filtros['nome_sala'],
            data_res=filtros['data_res'],
            busca=filtros['busca']
        )
        return render_template(
            'coordenador/painel_reserva.html',
            reservas=reservas,
            salas=buscar_salas(),
            sala_selecionada=filtros['nome_sala'],
            data_selecionada=filtros['data_res']
        )
    except Exception as e:
        flash(f'Erro ao listar reservas: {e}', 'danger')
        return redirect(url_for('coordenador_bp.painel_coordenador'))


@coordenador.route('/entregar_chave/<int:id_res>', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def entregar_chave(id_res):
    try:
        reserva_service.marcar_chave_entregue(id_res)
        flash('Chave marcada como ENTREGUE.', 'success')
    except Exception as e:
        flash(f'Erro ao marcar chave como entregue: {e}', 'danger')
    return redirect(url_for('coordenador_bp.listar_reservas'))


@coordenador.route('/devolver_chave/<int:id_res>', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def devolver_chave(id_res):
    try:
        reserva_service.marcar_chave_devolvida(id_res)
        flash('Chave marcada como DEVOLVIDA.', 'info')
    except Exception as e:
        flash(f'Erro ao marcar chave como devolvida: {e}', 'danger')
    return redirect(url_for('coordenador_bp.listar_reservas'))


@coordenador.route('/reservas/criar', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador'])
def criar_reserva():
    try:
        if request.method == 'POST':
            reserva_service.criar_reserva(
                nome_sala=request.form['nome_sala'],
                email=request.form['email'],
                data_res=request.form['data_res'],
                inicio=request.form['inicio'],
                termino=request.form['termino']
            )
            flash("Reserva criada com sucesso!", "success")
            return redirect(url_for('coordenador_bp.listar_reservas'))

        salas = reserva_service.buscar_nomes_salas()
    except Exception as e:
        flash(f"Erro ao criar reserva: {e}", "danger")
        salas = []

    return render_template('coordenador/criar_reserva.html', salas=salas)


@coordenador.route('/cancelar_reserva/<int:id_res>', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def cancelar_reserva(id_res):
    try:
        reserva_service.cancelar_reserva(id_res)
        flash('Reserva cancelada com sucesso.', 'warning')
    except Exception as e:
        flash(f'Erro ao cancelar reserva: {e}', 'danger')
    return redirect(url_for('coordenador_bp.listar_reservas'))
