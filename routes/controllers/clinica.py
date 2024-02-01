# controllers.py
from flask import jsonify, Blueprint, request
from injector import inject
from routes.middleware.token import token_required
from routes.usecases.clinica import ClinicaUseCase

clinica_bp = Blueprint('clinica', __name__)

@clinica_bp.route('/clinica', methods=['POST'])
@inject
def create_clinica(clinica_usecase: ClinicaUseCase):
    try:
        data = request.json
        nova_clinica = clinica_usecase.create_clinica(data)
        return jsonify({'message': 'Clínica criada com sucesso', 'data': nova_clinica}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@clinica_bp.route('/clinica', methods=['GET'])
@token_required
@inject
def get_clinicas(clinica_usecase: ClinicaUseCase):
    cnpj = request.args.get('cnpj')
    nome = request.args.get('nome')
    clinicas = clinica_usecase.get_clinicas(cnpj, nome)
    clinicas_list = [{'id': clinica.id, 'cnpj': clinica.cnpj, 'nome': clinica.nome} for clinica in clinicas]
    return jsonify(clinicas_list)

@clinica_bp.route('/clinica/<string:clinica_id>', methods=['PUT'])
@token_required
@inject
def update_clinica(clinica_id, clinica_usecase: ClinicaUseCase):
    try:
        data = request.json
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return jsonify({'error': 'Clínica não encontrada'}), 404
        clinica_atualizada = clinica_usecase.update_clinica(clinica, data)
        return jsonify({'message': 'Clínica atualizada com sucesso', 'data': clinica_atualizada}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@clinica_bp.route('/clinica/<string:clinica_id>', methods=['DELETE'])
@token_required
@inject
def delete_clinica(clinica_id, clinica_usecase: ClinicaUseCase):
    try:
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return jsonify({'error': 'Clínica não encontrada'}), 404
        clinica_usecase.delete_clinica(clinica)
        return jsonify({'message': 'Clínica excluída com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@clinica_bp.route('/clinica/<string:clinica_id>/medico', methods=['POST'])
@inject
def create_medico_clinica(clinica_id, medico_usecase: ClinicaUseCase):
    try:
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return jsonify({'message': 'Clínica não encontrada'}), 404
        data = request.json
        novo_medico = medico_usecase.create_medico(clinica, data)
        return jsonify({'message': 'Médico adicionado à clínica com sucesso', 'data': novo_medico}), 201
    except Exception as e:
        return jsonify({'message': 'Erro ao criar o médico', 'error': str(e)}), 400

@clinica_bp.route('/clinica/<string:clinica_id>/medico', methods=['GET'])
@inject
def get_medicos_clinica(clinica_id, medico_usecase: ClinicaUseCase):
    clinica = Clinica.query.get(clinica_id)
    if clinica:
        medicos = medico_usecase.get_medicos(clinica)
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
            } for medico in medicos
        ]
        return jsonify({"data": medicos_list})
    else:
        return jsonify({"mensagem": "Clínica não encontrada"}), 404

@clinica_bp.route('/clinica/<string:clinica_id>/medico', methods=['PUT'])
@inject
def update_medico_clinica(clinica_id, medico_usecase: ClinicaUseCase):
    try:
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return jsonify({'message': 'Clínica não encontrada'}), 404
        data = request.json
        medico_atualizado = medico_usecase.update_medico(clinica, data)
        return jsonify({'message': 'Médico atualizado com sucesso', 'data': medico_atualizado}), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao atualizar o médico', 'error': str(e)}), 400
