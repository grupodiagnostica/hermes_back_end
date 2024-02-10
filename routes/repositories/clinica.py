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

        clinicas = query.all()

        clinicas_list = [{'id': clinica.id, 'cnpj': clinica.cnpj, 'nome': clinica.nome} for clinica in clinicas]
        return clinicas_list

    def update_clinica(self, clinica_id, data):
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return 0
        for key, value in data.items():
            setattr(clinica, key, value)
        db.session.commit()
        return clinica

    def delete_clinica(self, clinica):
        db.session.delete(clinica)
        db.session.commit()

    def create_medico(self, clinica_id, data):
            clinica = Clinica.query.get(clinica_id)
            if not clinica:
                return 0
            senha_criptografada = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
            data['senha'] = senha_criptografada.decode('utf-8')
            novo_medico = Medico(**data)
            novo_medico.clinicas.append(clinica)
            db.session.add(novo_medico)
            db.session.commit()
            return novo_medico

    def get_medicos(self, clinica_id):
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return 0
        medicos_list = [
            {
                'id': medico.id,
                'id_pessoa': medico.id_pessoa,
                'crm': medico.crm,
                'especialidade': medico.especialidade,
                'senha': medico.senha,
                'email': medico.email,
                'foto_perfil': medico.foto_perfil,
                'pessoa': {
                    'id': medico.pessoa.id,
                    'cpf': medico.pessoa.cpf,
                    'data_nascimento': str(medico.pessoa.data_nascimento),
                    'nome': medico.pessoa.nome,
                    'telefone': medico.pessoa.telefone,
                    'cargo': medico.pessoa.cargo
                }
            } for medico in clinica.medicos
        ]
        return medicos_list

    def update_medico(self, clinica, data):
        medico = Medico.query.filter(Medico.crm == data['crm']).first()
        if not medico:
            return -1
        if clinica in medico.clinicas:
            return 0
        if medico and clinica not in medico.clinicas:
            medico.clinicas.append(clinica)
            db.session.commit()
        
        return 1

