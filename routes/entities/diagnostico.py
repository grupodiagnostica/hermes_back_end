from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Diagnostico(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    # id_modelo = db.Column(db.String(36), db.ForeignKey('modelo.id'), nullable=False)
    modelo = db.Column(db.String(255))
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'), nullable=False)
    id_medico = db.Column(db.String(36), db.ForeignKey('medico.id'), nullable=False)
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    raio_x = db.Column(db.Text)
    id_paciente = db.Column(db.String(36), db.ForeignKey('paciente.id'), nullable=False)
    laudo_medico = db.Column(db.Text)
    mapa_calor = db.Column(db.Text)
    resultado_modelo = db.Column(db.String(255))
    resultado_real = db.Column(db.String(255))

    def __init__(self, modelo,raio_x, id_medico, id_clinica, data_hora, id_paciente, laudo_medico, mapa_calor ,resultado_modelo, resultado_real ,id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
    
        self.modelo = modelo
        self.raio_x = raio_x
        self.id_medico = id_medico
        self.id_clinica = id_clinica
        self.data_hora = data_hora
        self.id_paciente = id_paciente
        self.laudo_medico = laudo_medico
        self.mapa_calor = mapa_calor
        self.resultado_modelo = resultado_modelo
        self.resultado_real = resultado_real