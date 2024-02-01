from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()
 
class Paciente(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    id_pessoa = db.Column(db.String(36), db.ForeignKey('pessoa.id'), nullable=False)
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    tipo_sanguineo = db.Column(db.String(5), nullable=False)
    detalhes_clinicos = db.Column(db.Text)
    cep = db.Column(db.String(50))
    logradouro = db.Column(db.String(100))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    numero = db.Column(db.String(10))
    estado = db.Column(db.String(2))
    diagnosticos = db.relationship('Diagnostico', backref='paciente', lazy=True)
    def __init__(self, id_pessoa,id_clinica, sexo, tipo_sanguineo, detalhes_clinicos, cep,logradouro, bairro, cidade, numero, estado, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.id_pessoa = id_pessoa
        self.id_clinica = id_clinica
        self.sexo = sexo
        self.tipo_sanguineo = tipo_sanguineo
        self.detalhes_clinicos = detalhes_clinicos
        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.numero = numero
        self.estado = estado