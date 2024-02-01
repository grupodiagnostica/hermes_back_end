from flask_sqlalchemy import SQLAlchemy
import uuid
from routes.entities.medico_clinica import medico_clinica_association

db = SQLAlchemy()

class Clinica(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True, nullable=False)
    foto_perfil = db.Column(db.Text, nullable=True)
    senha = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(50))
    logradouro = db.Column(db.String(100))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    numero = db.Column(db.String(10))
    estado = db.Column(db.String(2))
    medicos = db.relationship('Medico', secondary=medico_clinica_association, backref='clinica')
    funcionarios = db.relationship('Funcionario', backref='clinica', lazy=True)
    pacientes = db.relationship('Paciente', backref='clinica', lazy=True)
    diagnosticos = db.relationship('Diagnostico', backref='clinica', lazy=True)
    def __init__(self, cnpj, nome, senha,id=None, foto_perfil=None, telefone=None,email=None,logradouro=None,bairro=None,cidade=None
                 ,numero=None,estado=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.foto_perfil = foto_perfil
        self.cnpj = cnpj
        self.nome = nome
        self.senha = senha
        self.email = email
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.numero = numero
        self.estado = estado
        self.medicos = []