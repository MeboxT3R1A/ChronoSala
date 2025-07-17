# app/routes/coordenador/views.py
from flask import render_template, request, redirect, url_for, flash
from app.db import db # CORREÇÃO: Importe a instância 'db' do Flask-SQLAlchemy
                      # Agora 'db' é o seu objeto SQLAlchemy, não a função 'conectar'

# Importe os modelos que você usará neste Blueprint
# CERTIFIQUE-SE de que o caminho para models.py está correto.
# Se models.py está em 'app/models/', use 'from app.models.models import ...'
from app.models.models import Sala # Importa o modelo Sala

from . import coordenador_bp

@coordenador_bp.route('/')
def painel_coordenador():
    try:
        print("Tentando buscar salas com SQLAlchemy...")
        # Substitui: cursor.execute("SELECT * FROM sala")
        # Agora busca todos os objetos Sala
        salas = Sala.query.all()
        print("Dados recebidos (objetos Sala):", salas)
        return render_template('coordenador.html', salas=salas) # Use 'coordenador.html' conforme suas imagens

    except Exception as e:
        # Não é necessário db.session.rollback() para operações de leitura
        print(f"Erro ao acessar banco de dados: {e}")
        flash(f"Erro ao carregar salas: {e}", 'danger')
        # Certifique-se que 'geral_bp.index' é um endpoint válido para redirecionar em caso de erro
        return redirect(url_for('geral_bp.index'))


# NOTA: O ID da sala na sua DDL é 'nome_sala' (VARCHAR).
# Se você está usando 'id' (INT) no seu HTML/URLs, precisará ajustar para 'nome_sala'.
# Vou assumir 'nome_sala' como chave primária conforme seu modelo 'Sala'.
@coordenador_bp.route('/excluir/<string:nome_sala>', methods=['POST'])
def excluir_sala(nome_sala):
    try:
        # Substitui: cursor.execute("DELETE FROM sala WHERE id = %s", (id,))
        # Busca a sala pelo nome_sala (que é a chave primária)
        sala = Sala.query.get_or_404(nome_sala) # get_or_404 retorna 404 se não encontrar

        db.session.delete(sala) # Marca o objeto para ser excluído
        db.session.commit()     # Confirma a transação no banco de dados
        flash('Sala excluída com sucesso.', 'success')

    except Exception as e:
        db.session.rollback() # Em caso de erro, desfaz as operações na sessão
        flash(f'Erro ao excluir sala: {e}', 'danger')

    return redirect(url_for('coordenador_bp.painel_coordenador'))


# NOTA: Novamente, usando 'nome_sala' como chave primária para edição.
@coordenador_bp.route('/editar/<string:nome_sala>', methods=['GET', 'POST'])
def editar_sala(nome_sala):
    try:
        # Substitui: cursor.execute("SELECT * FROM sala WHERE id=%s", (id,))
        sala = Sala.query.get_or_404(nome_sala) # Busca a sala a ser editada

        if request.method == 'POST':
            # Obtém os dados do formulário
            novo_nome = request.form['nome_sala'] # O campo no formulário deve ser 'nome_sala'
            novo_status = request.form['status_sala'] # O campo no formulário deve ser 'status_sala'

            # Verifica se o nome da sala foi alterado e se o novo nome já existe
            if novo_nome != sala.nome_sala and Sala.query.get(novo_nome):
                flash(f'Erro: O nome da sala "{novo_nome}" já existe.', 'danger')
                return redirect(url_for('coordenador_bp.editar_sala', nome_sala=nome_sala))

            # Atualiza os atributos do objeto sala
            # CUIDADO: Se você permitir mudar a PK (nome_sala), é mais complexo.
            # O SQLAlchemy trata bem a mudança de PK, mas pode requerer uma nova instância
            # para evitar conflitos se o novo_nome já existir ANTES do commit.
            # Para simplificar, vou assumir que você está atualizando os campos.
            # Se 'nome_sala' pode ser alterado, o código deve ser mais robusto,
            # talvez deletando a antiga e criando uma nova, ou fazendo um UPDATE direto se for MySQL.
            # No MySQL, renomear uma PK string é um UPDATE.

            # Se o nome da sala (PK) pode ser alterado:
            if novo_nome != sala.nome_sala:
                # Flask-SQLAlchemy pode lidar com isso, mas é mais direto em alguns casos
                # executar um update explícito para PKs STRING
                db.session.query(Sala).filter_by(nome_sala=sala.nome_sala).update(
                    {'nome_sala': novo_nome, 'status_sala': novo_status}
                )
                sala.nome_sala = novo_nome # Atualiza o objeto em memória para refletir a mudança
            else:
                sala.status_sala = novo_status # Atualiza apenas o status se o nome não mudou

            # Sua DDL não tem campo 'imagem' na tabela 'sala'.
            # Se você tinha 'imagem' antes, ele foi removido dos modelos.
            # Remova ou adicione 'imagem' de volta ao seu modelo 'Sala' se for necessário.
            # sala.imagem = request.form['imagem'] # Descomente se 'imagem' for adicionado ao modelo Sala

            db.session.commit() # Salva as alterações no banco de dados
            flash('Sala atualizada com sucesso.', 'success')
            # Redireciona para o painel ou para a página de edição com o NOVO nome_sala
            return redirect(url_for('coordenador_bp.painel_coordenador'))

        # Para requisição GET, renderiza o formulário de edição
        imagens = ['img1.png', 'img2.png', 'img3.png'] # Atualize com imagens reais
        return render_template('editar_sala.html', sala=sala, imagens=imagens)

    except Exception as e:
        db.session.rollback() # Desfaz a transação em caso de erro
        flash(f'Erro ao editar sala: {e}', 'danger')
        return redirect(url_for('coordenador_bp.painel_coordenador'))


# Exemplo de rota para adicionar uma nova sala (baseado em campos da sua DDL 'sala')
@coordenador_bp.route('/adicionar_sala', methods=['GET', 'POST'])
def adicionar_sala():
    if request.method == 'POST':
        try:
            nome_sala = request.form['nome_sala']
            status_sala = request.form['status_sala'] # 'disponivel', 'reservado', 'manutenção'

            # Opcional: Validar se o nome_sala já existe antes de adicionar
            if Sala.query.get(nome_sala):
                flash(f'Erro: A sala "{nome_sala}" já existe.', 'danger')
                return redirect(url_for('coordenador_bp.adicionar_sala'))

            # Cria uma nova instância do modelo Sala
            nova_sala = Sala(
                nome_sala=nome_sala,
                status_sala=status_sala
            )

            db.session.add(nova_sala) # Adiciona o objeto à sessão do SQLAlchemy
            db.session.commit()       # Confirma a transação, salvando no banco de dados
            flash('Sala adicionada com sucesso!', 'success')
            return redirect(url_for('coordenador_bp.painel_coordenador'))
        except Exception as e:
            db.session.rollback() # Desfaz a transação em caso de erro
            flash(f'Erro ao adicionar sala: {e}', 'danger')

    # Para requisição GET, apenas renderiza o formulário de adição
    return render_template('adicionar_sala.html') # Você precisará criar este template