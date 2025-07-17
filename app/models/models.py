# app/models/models.py
from app.db import db # CORREÇÃO: Importe a instância 'db' de dentro do pacote 'app'
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum

# Modelo para a tabela 'funcionario'
class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    email = db.Column(db.String(60), primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    matricula = db.Column(db.CHAR(5), unique=True, nullable=True) # Sua DDL diz CHAR(5) UNIQUE, mas não NOT NULL.
    senha = db.Column(db.String(128), nullable=False) # Aumentei para 128 para hashes de senha (ideal)
    funcao = db.Column(db.String(25), nullable=False) # 'Administrador', 'Coordenador', 'Instrutor'

    # Relacionamentos
    # Um funcionário pode ter múltiplos CEPs associados
    ceps_associados = db.relationship('CepFunc', backref='funcionario_cep', lazy=True, cascade="all, delete-orphan")
    # Um funcionário pode ter muitas reservas
    reservas = db.relationship('Reserva', backref='funcionario_reserva', lazy=True, cascade="all, delete-orphan")
    # Um funcionário pode ter muitas entradas de histórico
    historicos = db.relationship('Historico', backref='funcionario_historico', lazy=True, cascade="all, delete-orphan")
    # Um funcionário (professor) pode estar em múltiplos controles de chaves
    controle_chaves_prof = db.relationship('ControleChaves', backref='professor_chave', lazy=True, cascade="all, delete-orphan")


    def set_password(self, password):
        """Define a senha, armazenando o hash."""
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash."""
        return check_password_hash(self.senha, password)

    def __repr__(self):
        return f"<Funcionario {self.nome} ({self.email})>"

# Modelo para a tabela 'cep'
class Cep(db.Model):
    __tablename__ = 'cep'
    nome = db.Column(db.String(40), primary_key=True) # 'nome' do CEP é a chave primária
    endereco = db.Column(db.String(50), nullable=False)

    # Relacionamento: Um CEP pode ter múltiplos cep_func
    funcionarios_cep_func = db.relationship('CepFunc', backref='cep_referencia', lazy=True, cascade="all, delete-orphan")
    # Um CEP pode ter muitas entradas de histórico (se o histórico se refere ao nome do CEP)
    historicos = db.relationship('Historico', backref='cep_historico', lazy=True) # Não cascade, pois 'cep' é entidade mestre

    def __repr__(self):
        return f"<Cep {self.nome} ({self.endereco})>"

# Modelo para a tabela 'cep_func' (Tabela de Associação)
class CepFunc(db.Model):
    __tablename__ = 'cep_func'
    cep_func_id = db.Column(db.Integer, primary_key=True, autoincrement=True, name='cep_func') # Use 'name' para mapear 'cep_func' como nome da coluna
    email = db.Column(db.String(60), db.ForeignKey('funcionario.email', ondelete='CASCADE'), nullable=True) # Permiti nullable=True se a DDL não força NOT NULL
    nome = db.Column(db.String(40), db.ForeignKey('cep.nome', ondelete='CASCADE'), nullable=True) # Permiti nullable=True

    def __repr__(self):
        return f"<CepFunc ID: {self.cep_func_id} - Func: {self.email}, CEP: {self.nome}>"

# Modelo para a tabela 'sala'
class Sala(db.Model):
    __tablename__ = 'sala'
    nome_sala = db.Column(db.String(150), primary_key=True, nullable=False)
    status_sala = db.Column(Enum('reservado', 'disponivel', 'manutenção', name='status_sala_enum'),
                           default='disponivel', nullable=False)

    # Relacionamento: Uma Sala pode ter muitas reservas
    reservas = db.relationship('Reserva', backref='sala_reservada', lazy=True, cascade="all, delete-orphan")
    # Uma Sala pode ter muitas entradas de histórico
    historicos = db.relationship('Historico', backref='sala_historico', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sala {self.nome_sala} ({self.status_sala})>"

# Modelo para a tabela 'cursos'
class Curso(db.Model): # Renomeado para Curso (singular)
    __tablename__ = 'cursos'
    id_cursos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    segmento = db.Column(db.String(150), nullable=False)

    # Relacionamento: Um Curso pode ter muitas entradas de histórico
    historicos = db.relationship('Historico', backref='curso_historico', lazy=True) # Não cascade, pois 'curso' é entidade mestre

    def __repr__(self):
        return f"<Curso {self.nome} ({self.segmento})>"

# Modelo para a tabela 'reserva'
class Reserva(db.Model):
    __tablename__ = 'reserva'
    id_res = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_sala = db.Column(db.String(150), db.ForeignKey('sala.nome_sala', onupdate='CASCADE', ondelete='CASCADE'), nullable=True) # Sua DDL não tem NOT NULL para nome_sala
    email = db.Column(db.String(60), db.ForeignKey('funcionario.email', onupdate='CASCADE', ondelete='CASCADE'), nullable=True) # Sua DDL não tem NOT NULL para email
    inicio = db.Column(db.Time, nullable=False)
    termino = db.Column(db.Time, nullable=False)
    data_res = db.Column(db.Date, nullable=False)
    status_res = db.Column(Enum('reservado', 'cancelado', name='status_res_enum'), default='reservado', nullable=True) # Sua DDL não tem NOT NULL
    status_chave = db.Column(Enum('pendente', 'entregue', 'devolvida', name='status_chave_enum'), default='pendente', nullable=True) # Sua DDL não tem NOT NULL

    # CONSTRAINT chk_horario CHECK (inicio < termino) - Flask-SQLAlchemy não mapeia CHECK constraints diretamente.
    # Você deve implementar essa validação na sua lógica da aplicação (ex: antes de adicionar a reserva).

    # Relacionamento: Uma Reserva pode ter uma entrada de controle de chaves
    controle_chave = db.relationship('ControleChaves', backref='reserva_controle', uselist=False, lazy=True, cascade="all, delete-orphan")
    # Uma Reserva pode ter muitas entradas de histórico
    historicos = db.relationship('Historico', backref='reserva_historico', lazy=True, cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Reserva ID: {self.id_res} - Sala: {self.nome_sala} - Data: {self.data_res}>"

# Modelo para a tabela 'historico'
class Historico(db.Model):
    __tablename__ = 'historico'
    id_historico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_historico = db.Column(db.DateTime, nullable=False)

    # Chaves estrangeiras, permiti nullable=True conforme sua DDL
    nome = db.Column(db.String(40), db.ForeignKey('cep.nome'), nullable=True)
    email = db.Column(db.String(60), db.ForeignKey('funcionario.email', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    id_res = db.Column(db.Integer, db.ForeignKey('reserva.id_res', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    nome_sala = db.Column(db.String(150), db.ForeignKey('sala.nome_sala', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    id_cursos = db.Column(db.Integer, db.ForeignKey('cursos.id_cursos'), nullable=True)

    def __repr__(self):
        return f"<Historico ID: {self.id_historico} - Data: {self.data_historico}>"

# Modelo para a tabela 'controle_chaves'
class ControleChaves(db.Model):
    __tablename__ = 'controle_chaves'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_reserva = db.Column(db.Integer, db.ForeignKey('reserva.id_res', onupdate='CASCADE', ondelete='CASCADE'), nullable=True) # Sua DDL não tem NOT NULL
    email_professor = db.Column(db.String(60), db.ForeignKey('funcionario.email', onupdate='CASCADE', ondelete='CASCADE'), nullable=True) # Sua DDL não tem NOT NULL
    data_entrega = db.Column(db.DateTime, nullable=True) # Sua DDL não tem NOT NULL
    data_devolucao = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<ControleChaves ID: {self.id} - Reserva: {self.id_reserva}>"