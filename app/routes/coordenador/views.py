# app/routes/coordenador/views.py
from flask import render_template, request, redirect, url_for, flash
from app.models.db import db
from app.models.models import Sala, StatusSalaEnum  # ✅ Enum importado

from . import coordenador_bp

@coordenador_bp.route('/')
def painel_coordenador():
    try:
        salas = Sala.query.all()
        return render_template('coordenador.html', salas=salas)
    except Exception as e:
        flash(f"Erro ao carregar salas: {e}", 'danger')
        return redirect(url_for('geral.index'))

@coordenador_bp.route('/excluir/<string:nome_sala>', methods=['POST'])
def excluir_sala(nome_sala):
    try:
        sala = Sala.query.get_or_404(nome_sala)
        db.session.delete(sala)
        db.session.commit()
        flash('Sala excluída com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir sala: {e}', 'danger')
    return redirect(url_for('coordenador_bp.painel_coordenador'))

@coordenador_bp.route('/editar/<string:nome_sala>', methods=['GET', 'POST'])
def editar_sala(nome_sala):
    try:
        sala = Sala.query.get_or_404(nome_sala)

        if request.method == 'POST':
            novo_nome = request.form['nome_sala']
            novo_status = StatusSalaEnum(request.form['status_sala'])  # ✅ Enum convertido corretamente

            if novo_nome != sala.nome_sala and Sala.query.get(novo_nome):
                flash(f'Erro: O nome da sala "{novo_nome}" já existe.', 'danger')
                return redirect(url_for('coordenador_bp.editar_sala', nome_sala=nome_sala))

            if novo_nome != sala.nome_sala:
                db.session.query(Sala).filter_by(nome_sala=sala.nome_sala).update(
                    {'nome_sala': novo_nome, 'status_sala': novo_status}
                )
                sala.nome_sala = novo_nome
            else:
                sala.status_sala = novo_status

            db.session.commit()
            flash('Sala atualizada com sucesso.', 'success')
            return redirect(url_for('coordenador_bp.painel_coordenador'))

        imagens = ['img1.png', 'img2.png', 'img3.png']
        return render_template('editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao editar sala: {e}', 'danger')
        return redirect(url_for('coordenador_bp.painel_coordenador'))

@coordenador_bp.route('/adicionar_sala', methods=['GET', 'POST'])
def adicionar_sala():
    if request.method == 'POST':
        try:
            nome_sala = request.form['nome_sala']
            status_sala = StatusSalaEnum(request.form['status_sala'])  # ✅ Enum convertido corretamente

            if Sala.query.get(nome_sala):
                flash(f'Erro: A sala "{nome_sala}" já existe.', 'danger')
                return redirect(url_for('coordenador_bp.adicionar_sala'))

            nova_sala = Sala(
                nome_sala=nome_sala,
                status_sala=status_sala
            )

            db.session.add(nova_sala)
            db.session.commit()
            flash('Sala adicionada com sucesso!', 'success')
            return redirect(url_for('coordenador_bp.painel_coordenador'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar sala: {e}', 'danger')

    return render_template('adicionar_sala.html')
