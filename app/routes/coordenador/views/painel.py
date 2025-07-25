# app/routes/coordenador/views/painel.py

from flask import render_template, flash
from app.decorators import login_required, role_required
from app.routes.coordenador import coordenador_bp as coordenador
from app.routes.coordenador.services.coordenador_service import buscar_salas

@coordenador.route('/')
@login_required
@role_required(['Coordenador'])
def painel_coordenador():
    try:
        salas = buscar_salas()
        return render_template('coordenador/coordenador.html', salas=salas)
    except Exception as e:
        flash(f'Erro ao acessar salas: {e}', 'error')
        return render_template('erro/erro_generico.html', erro=str(e))
