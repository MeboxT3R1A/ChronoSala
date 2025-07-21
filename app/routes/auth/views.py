# app/routes/auth/views.py
from flask import render_template, request, redirect, url_for, flash, session
from app.db import get_db, close_db # Importa as funções para interagir com o banco de dados
from . import login_bp # Importa o Blueprint do login
from werkzeug.security import check_password_hash # Importa para verificar senhas hash

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    """
    Rota para o formulário de login e processamento da autenticação.
    Permite métodos GET (para exibir o formulário) e POST (para processar o envio do formulário).
    """
    # Verifica se a requisição é um POST, o que indica que o formulário foi submetido.
    if request.method == 'POST':
        # Pega os valores dos campos 'usuario' (email ou matrícula) e 'senha' do formulário.
        # request.form é um dicionário que contém os dados do formulário submetido via POST.
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Inicializa a variável para armazenar o funcionário encontrado no banco.
        funcionario = None
        # Inicializa a variável para preencher o campo de usuário caso o login falhe.
        usuario_preenchido = usuario

        # Tenta estabelecer uma conexão com o banco de dados e executar a consulta.
        try:
            db = get_db()  # Obtém a conexão com o banco de dados.
            cursor = db.cursor() # Cria um objeto cursor para executar comandos SQL.

            # Consulta o banco de dados para encontrar um funcionário correspondente
            # pelo email ou matrícula. O uso de %s é para evitar injeção de SQL,
            # onde os valores são passados como uma tupla para o execute().
            # Aqui estamos procurando por email OU matrícula.
            query = "SELECT email, nome, funcao, senha FROM funcionario WHERE email = %s OR matricula = %s"
            cursor.execute(query, (usuario, usuario)) # Passa o 'usuario' duas vezes para cobrir email ou matrícula

            # fetchone() recupera apenas a próxima linha de um conjunto de resultados da consulta, ou None se não houver mais linhas.
            funcionario = cursor.fetchone()

            # close_db() é chamado no teardown_appcontext, mas se você quiser fechar imediatamente
            # após esta operação, pode ser feito aqui, embora geralmente seja gerenciado pelo Flask.
            # close_db() # Geralmente não é necessário chamar aqui se o Flask gerencia o teardown.

            # Verifica se um funcionário foi encontrado e se a senha está correta.
            # check_password_hash() é usado para comparar a senha fornecida pelo usuário
            # com o hash da senha armazenado no banco de dados.
            if funcionario and check_password_hash(funcionario['senha'], senha):
                # Se o login for bem-sucedido, define variáveis de sessão.
                # A sessão é um dicionário que armazena dados específicos do usuário
                # entre requisições. Flask assina criptograficamente as cookies de sessão.
                session['logged_in'] = True
                session['user_email'] = funcionario['email']
                session['user_name'] = funcionario['nome']
                session['user_role'] = funcionario['funcao'] # Armazena a função do usuário na sessão

                # flash() é usado para enviar mensagens unidirecionais para o próximo template renderizado.
                # 'success' é uma categoria que pode ser usada para estilizar a mensagem.
                flash(f'Bem-vindo(a) {funcionario["nome"]}!', 'success')

                # Redireciona o usuário para a página apropriada com base na sua função.
                # url_for() gera uma URL para a função de view especificada,
                # garantindo que as URLs sejam dinâmicas e corretas.
                if funcionario['funcao'] == 'Coordenador':
                    return redirect(url_for('coordenador_bp.painel_coordenador'))
                elif funcionario['funcao'] == 'Instrutor':
                    return redirect(url_for('instrutor_bp.painel_instrutor'))
                elif funcionario['funcao'] == 'Administrador':
                    # Embora você tenha um 'Administrador' na inserção SQL, seu código original
                    # redirecionava para o painel do instrutor. Mantenho isso por enquanto.
                    return redirect(url_for('instrutor_bp.painel_instrutor')) # Ou para uma página admin dedicada
                else:
                    # Caso a função não seja reconhecida, redireciona para uma página padrão.
                    flash('Função de usuário não reconhecida. Redirecionando para a página inicial.', 'warning')
                    return redirect(url_for('geral_bp.home'))
            else:
                # Se o funcionário não for encontrado ou a senha estiver incorreta.
                flash('E-mail, matrícula ou senha inválidos. Por favor, tente novamente.', 'error')
                # Renderiza o template de login novamente, mantendo o campo de usuário preenchido.
                return render_template('login.html', usuario_preenchido=usuario_preenchido)

        except Exception as e:
            # Captura qualquer exceção que ocorra durante a interação com o banco de dados.
            flash(f'Erro interno do servidor: {e}', 'error')
            # Você pode logar o erro para depuração em um ambiente real: app.logger.error(f"Erro de DB: {e}")
            return render_template('login.html', usuario_preenchido=usuario_preenchido)

    # Se a requisição for GET, apenas renderiza o formulário de login vazio.
    return render_template('login.html', usuario_preenchido='')