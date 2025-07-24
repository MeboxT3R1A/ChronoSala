# app/routes/auth/services/session_manager.py
from flask import session

def salvar_sessao(funcionario):
    session['logged_in'] = True
    session['user_role'] = funcionario['funcao']
    session['user_name'] = funcionario['nome']
    print("DEBUG - Sessão salva:", dict(session))

def limpar_sessao():
    session.clear()

def destino_por_funcao(funcao):
    destinos = {
        'Coordenador': 'coordenador_bp.painel_coordenador',
        'Instrutor': 'instrutor_bp.painel_instrutor',
    }
    return destinos.get(funcao)
