# repositories.py
from models import db, Clinica, Medico
import bcrypt

class ClinicaRepository:
    def create_clinica(self, data):
        senha_criptografada = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        data['senha'] = senha_criptografada.decode('utf-8')
        nova_clinica = Clinica(**data)
        db.session.add(nova_clinica)
        db.session.commit()
        return nova_clinica

    def get_clinicas(self, cnpj=None, nome=None):
        query = Clinica.query
        if cnpj:
            query = query.filter(Clinica.cnpj == cnpj)
        if nome:
            query = query.filter(Clinica.nome.ilike(f"%{nome}%"))
        return query.all()

    def update_clinica(self, clinica, data):
        for key, value in data.items():
            setattr(clinica, key, value)
        db.session.commit()
        return clinica

    def delete_clinica(self, clinica):
        db.session.delete(clinica)
        db.session.commit()

    def create_medico(self, clinica, data):
            senha_criptografada = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
            data['senha'] = senha_criptografada.decode('utf-8')
            novo_medico = Medico(**data)
            novo_medico.clinicas.append(clinica)
            db.session.add(novo_medico)
            db.session.commit()
            return novo_medico

    def get_medicos(self, clinica):
        return clinica.medicos

    def update_medico(self, clinica, data):
        medico = Medico.query.filter(Medico.crm == data['crm']).first()
        if medico and clinica not in medico.clinicas:
            medico.clinicas.append(clinica)
            db.session.commit()
        return medico
