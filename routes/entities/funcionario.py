from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Funcionario(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    id_pessoa = db.Column(db.String(36), db.ForeignKey('pessoa.id'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    especialista = db.Column(db.String(100))
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'))

    def __init__(self, id_pessoa, email, senha, especialista, id_clinica, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.id_pessoa = id_pessoa
        self.email = email
        self.senha = senha
        self.especialista = especialista
        self.id_clinica = id_clinica