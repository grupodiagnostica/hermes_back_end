from models import db, Medico
import bcrypt

class MedicoRepository:
    def create_medico(self, data):
        senha_criptografada = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        data['senha'] = senha_criptografada.decode('utf-8')
        novo_medico = Medico(**data)
        db.session.add(novo_medico)
        db.session.commit()
        return novo_medico

    def get_medicos(self, id_pessoa=None, crm=None, especialidade=None):
        query = Medico.query
        if id_pessoa:
            query = query.filter(Medico.id_pessoa == id_pessoa)
        if crm:
            query = query.filter(Medico.crm == crm)
        if especialidade:
            query = query.filter(Medico.especialidade == especialidade)

        medicos = query.all()

        medicos_list = [{
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
        } for medico in medicos]

        return medicos_list

    def update_medico(self, medico_id, data):
        medico = Medico.query.get(medico_id)
        if not medico:
            return {'error': 'Médico não encontrado'}, 404

        for key, value in data.items():
            setattr(medico, key, value)

        db.session.commit()

        medico_atualizado = {
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
        }

        return medico_atualizado

    def delete_medico(self, medico_id):
        medico = Medico.query.get(medico_id)
        if not medico:
            return {'error': 'Médico não encontrado'}, 404

        db.session.delete(medico)
        db.session.commit()

        return {'message': 'Médico excluído com sucesso'}

    def get_clinicas_medico(self, medico_id):
        medico = Medico.query.get(medico_id)
        if not medico:
            return {'error': 'Médico não encontrado'}, 404

        clinicas_list = [{
            'id': clinica.id,
            'cep': clinica.cep,
            'cnpj': clinica.cnpj,
            'email': clinica.email,
            'nome': clinica.nome,
            'foto_perfil': clinica.foto_perfil
        } for clinica in medico.clinicas]

        return clinicas_list

    def existe_medico(self, medico_crm):
        medico = Medico.query.filter(Medico.crm == medico_crm).first()
        if medico:
            medicoJson = {
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
            }
            return {'result': 1, 'data': medicoJson}, 200

        return {'result': 0}, 200
