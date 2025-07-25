from flask import (
    render_template, request,
    redirect, url_for, flash
)
from app.routes.coordenador import coordenador_bp as coordenador
from app.decorators import login_required, role_required
from app.routes.coordenador.services.sala_services import (
    buscar_sala_por_nome,
    atualizar_status_sala,
    excluir_sala_por_nome,
    adicionar_sala_db
)
import pymysql

@coordenador.route('/editar/<nome_sala>', methods=['GET', 'POST'])
@login_required
@role_required(['Coordenador'])
def editar_sala(nome_sala):
    try:
        if request.method == 'POST':
            status = request.form['status']
            atualizar_status_sala(nome_sala, status)
            flash('Sala atualizada com sucesso.', 'success')
            return redirect(url_for('coordenador_bp.painel_coordenador'))

        sala = buscar_sala_por_nome(nome_sala)
        if not sala:
            flash('Sala não encontrada.', 'warning')
            return redirect(url_for('coordenador_bp.painel_coordenador'))

        imagens = ['img1.png', 'img2.png', 'img3.png']
        return render_template('coordenador/editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        flash(f'Erro ao editar sala: {e}', 'error')
        return redirect(url_for('coordenador_bp.painel_coordenador'))

@coordenador.route('/excluir/<nome_sala>', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def excluir_sala(nome_sala):
    try:
        excluir_sala_por_nome(nome_sala)
        flash('Sala excluída com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao excluir sala: {e}', 'error')

    return redirect(url_for('coordenador_bp.painel_coordenador'))

@coordenador.route('/adicionar_sala', methods=['POST'])
@login_required
@role_required(['Coordenador'])
def adicionar_sala():
    try:
        nome_sala = request.form['nome_sala']
        status_sala = request.form['status_sala']
        adicionar_sala_db(nome_sala, status_sala)
        flash('Sala adicionada com sucesso!', 'success')
    except pymysql.err.IntegrityError:
        flash('Esta sala já existe!', 'error')
    except Exception as e:
        flash(f'Erro ao adicionar sala: {e}', 'error')

    return redirect(url_for('coordenador_bp.painel_coordenador'))
