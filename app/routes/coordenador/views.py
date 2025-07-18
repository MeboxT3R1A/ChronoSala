from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from app.routes.coordenador import coordenador_bp as coordenador

@coordenador.route('/')
def painel_coordenador():
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM sala")
            salas = cursor.fetchall()
        return render_template('coordenador.html', salas=salas)

    except Exception as e:
        print("Erro ao acessar banco:", e)
        return f"Erro ao acessar banco de dados: {e}"


@coordenador.route('/excluir/<nome_sala>', methods=['POST'])
def excluir_sala(nome_sala):
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM sala WHERE nome_sala = %s", (nome_sala,))
            conn.commit()
            flash('Sala excluída com sucesso.')

    except Exception as e:
        flash(f'Erro ao excluir sala: {e}')

    return redirect(url_for('coordenador.painel_coordenador'))


@coordenador.route('/editar/<nome_sala>', methods=['GET', 'POST'])
def editar_sala(nome_sala):
    try:
        conn = get_db()
        with conn.cursor() as cursor:

            if request.method == 'POST':
                status = request.form['status']
                cursor.execute(
                    "UPDATE sala SET status_sala=%s WHERE nome_sala=%s",
                    (status, nome_sala)
                )
                conn.commit()
                flash('Sala atualizada com sucesso.')
                return redirect(url_for('coordenador.painel_coordenador'))

            cursor.execute("SELECT * FROM sala WHERE nome_sala=%s", (nome_sala,))
            sala = cursor.fetchone()

            if not sala:
                flash('Sala não encontrada.')
                return redirect(url_for('coordenador.painel_coordenador'))

        imagens = ['img1.png', 'img2.png', 'img3.png']  # se usar imagens
        return render_template('editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        flash(f'Erro ao editar sala: {e}')
        return redirect(url_for('coordenador.painel_coordenador'))
