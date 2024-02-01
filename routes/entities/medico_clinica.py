from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

medico_clinica_association = db.Table(
    'medico_clinica_association',
    db.Column('medico_id', db.String(36), db.ForeignKey('medico.id')),
    db.Column('clinica_id', db.String(36), db.ForeignKey('clinica.id'))
)