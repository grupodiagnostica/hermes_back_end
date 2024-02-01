from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Administrador(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    def __init__(self, senha, username, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.senha = senha
        self.username = username