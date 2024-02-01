from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Pessoa(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15))
    cargo = db.Column(db.String(100))
    pacientes = db.relationship('Paciente', backref='pessoa', lazy=True)
    funcionarios = db.relationship('Funcionario', backref='pessoa', lazy=True)
    medicos = db.relationship('Medico', backref='pessoa', lazy=True)
    def __init__(self, cpf, data_nascimento, nome, telefone, cargo, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.nome = nome
        self.telefone = telefone
        self.cargo = cargo