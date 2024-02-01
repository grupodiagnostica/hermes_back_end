from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Modelo(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(100), nullable=False)
    precisao = db.Column(db.String(15))
    acuracia = db.Column(db.String(15))
    f1score = db.Column(db.String(15))
    recall = db.Column(db.String(15))
    kappa = db.Column(db.String(15))
    filtros = db.Column(db.String(510))
    dataAugmentation = db.Column(db.Boolean, default=False)
    tipoImagem = db.Column(db.String(15))

    def __init__(self, precisao, acuracia, f1score, recall, kappa, filtros, dataAugmentation, tipoImagem, cnpj, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.cnpj = cnpj
        self.precisao = precisao
        self.acuracia = acuracia
        self.f1score = f1score
        self.recall = recall
        self.kappa = kappa
        self.filtros = filtros
        self.dataAugmentation = dataAugmentation
        self.tipoImagem = tipoImagem