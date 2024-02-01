from flask_sqlalchemy import SQLAlchemy
import uuid
from routes.entities.medico_clinica import medico_clinica_association

db = SQLAlchemy()

class Medico(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    id_pessoa = db.Column(db.String(36), db.ForeignKey('pessoa.id'), nullable=False)
    crm = db.Column(db.String(15), unique=True, nullable=False)
    especialidade = db.Column(db.String(100))
    senha = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    foto_perfil = db.Column(db.Text, nullable=True)
    verification_code = db.Column(db.String(6), nullable=True)
    verification_code_expiration = db.Column(db.DateTime, nullable=True)
    clinicas = db.relationship('Clinica', secondary=medico_clinica_association, backref='medico')
    diagnosticos = db.relationship('Diagnostico', backref='medico', lazy=True)
    def __init__(self, id_pessoa, crm, especialidade, senha, email, id=None, foto_perfil=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        if  foto_perfil is None:
            self.foto_perfil = None
        else:
            self.foto_perfil = foto_perfil
        self.id_pessoa = id_pessoa
        self.crm = crm 
        self.especialidade = especialidade
        self.senha = senha
        self.email = email
        self.clinicas = []