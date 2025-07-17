from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, CheckConstraint, ForeignKey
from datetime import datetime
import enum
from app.models.db import db  # Importa a instância 'db' do Flask-SQLAlchemy

# Enums usados no modelo
class StatusSalaEnum(enum.Enum):
    reservado = 'reservado'
    disponivel = 'disponivel'
    manutencao = 'manutenção'

class StatusReservaEnum(enum.Enum):
    reservado = 'reservado'
    cancelado = 'cancelado'

class StatusChaveEnum(enum.Enum):
    pendente = 'pendente'
    entregue = 'entregue'
    devolvida = 'devolvida'


class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    email = db.Column(db.String(60), primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    matricula = db.Column(db.String(5), unique=True)
    senha = db.Column(db.String(11), nullable=False)
    funcao = db.Column(db.String(25), nullable=False)

    reservas = db.relationship('Reserva', backref='funcionario', cascade='all, delete-orphan')
    historicos = db.relationship('Historico', backref='funcionario', cascade='all, delete-orphan')
    chaves = db.relationship('ControleChaves', backref='professor', cascade='all, delete-orphan')
    ceps = db.relationship('CepFunc', backref='funcionario', cascade='all, delete-orphan')


class Cep(db.Model):
    __tablename__ = 'cep'
    nome = db.Column(db.String(40), primary_key=True)
    endereco = db.Column(db.String(50), nullable=False)

    ceps_func = db.relationship('CepFunc', backref='cep', cascade='all, delete-orphan')
    historicos = db.relationship('Historico', backref='cep', cascade='all, delete-orphan')


class CepFunc(db.Model):
    __tablename__ = 'cep_func'
    cep_func = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), db.ForeignKey('funcionario.email', ondelete='CASCADE'))
    nome = db.Column(db.String(40), db.ForeignKey('cep.nome'))


class Sala(db.Model):
    __tablename__ = 'sala'
    nome_sala = db.Column(db.String(150), primary_key=True)
    status_sala = db.Column(Enum(StatusSalaEnum), default=StatusSalaEnum.disponivel)

    reservas = db.relationship('Reserva', backref='sala', cascade='all, delete-orphan')
    historicos = db.relationship('Historico', backref='sala', cascade='all, delete-orphan')


class Cursos(db.Model):
    __tablename__ = 'cursos'
    id_cursos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    segmento = db.Column(db.String(150), nullable=False)

    historicos = db.relationship('Historico', backref='curso', cascade='all, delete-orphan')


class Reserva(db.Model):
    __tablename__ = 'reserva'
    id_res = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_sala = db.Column(db.String(150), db.ForeignKey('sala.nome_sala', ondelete='CASCADE', onupdate='CASCADE'))
    email = db.Column(db.String(60), db.ForeignKey('funcionario.email', ondelete='CASCADE', onupdate='CASCADE'))
    inicio = db.Column(db.Time, nullable=False)
    termino = db.Column(db.Time, nullable=False)
    data_res = db.Column(db.Date, nullable=False)
    status_res = db.Column(Enum(StatusReservaEnum), default=StatusReservaEnum.reservado)
    status_chave = db.Column(Enum(StatusChaveEnum), default=StatusChaveEnum.pendente)

    __table_args__ = (
        CheckConstraint('inicio < termino', name='chk_horario'),
    )

    historicos = db.relationship('Historico', backref='reserva', cascade='all, delete-orphan')
    chaves = db.relationship('ControleChaves', backref='reserva', cascade='all, delete-orphan')


class Historico(db.Model):
    __tablename__ = 'historico'
    id_historico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_historico = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nome = db.Column(db.String(40), db.ForeignKey('cep.nome'))
    email = db.Column(db.String(60), db.ForeignKey('funcionario.email', ondelete='CASCADE', onupdate='CASCADE'))
    id_res = db.Column(db.Integer, db.ForeignKey('reserva.id_res', ondelete='CASCADE', onupdate='CASCADE'))
    nome_sala = db.Column(db.String(150), db.ForeignKey('sala.nome_sala', ondelete='CASCADE', onupdate='CASCADE'))
    id_cursos = db.Column(db.Integer, db.ForeignKey('cursos.id_cursos'))


class ControleChaves(db.Model):
    __tablename__ = 'controle_chaves'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_reserva = db.Column(db.Integer, db.ForeignKey('reserva.id_res', ondelete='CASCADE', onupdate='CASCADE'))
    email_professor = db.Column(db.String(60), db.ForeignKey('funcionario.email', ondelete='CASCADE', onupdate='CASCADE'))
    data_entrega = db.Column(db.DateTime)
    data_devolucao = db.Column(db.DateTime)
