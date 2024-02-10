# controllers.py
from flask import jsonify, Blueprint, request
from injector import inject
from models import Clinica
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
    clinicas_list = clinica_usecase.get_clinicas(cnpj, nome)
    return jsonify(clinicas_list)

@clinica_bp.route('/clinica/<string:clinica_id>', methods=['PUT'])
@token_required
@inject
def update_clinica(clinica_id, clinica_usecase: ClinicaUseCase):
    try:
        data = request.json
        clinica_atualizada = clinica_usecase.update_clinica(clinica_id, data)
        if clinica_atualizada == 0:
            return jsonify({'error': 'Clínica não encontrada'}), 404
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
        data = request.json
        novo_medico = medico_usecase.create_medico(clinica_id, data)
        if novo_medico == 0:
            return jsonify({'message': 'Clínica não encontrada'}), 404
        return jsonify({'message': 'Médico adicionado à clínica com sucesso', 'data': novo_medico}), 201
    except Exception as e:
        return jsonify({'message': 'Erro ao criar o médico', 'error': str(e)}), 400

@clinica_bp.route('/clinica/<string:clinica_id>/medico', methods=['GET'])
@inject
def get_medicos_clinica(clinica_id, medico_usecase: ClinicaUseCase):
    try:
        medicos_list = medico_usecase.get_medicos(clinica_id)
        return jsonify({"data": medicos_list})
    except Exception as e:
        return jsonify({'message': 'Erro ao listar médicos', 'error': str(e)}), 400


@clinica_bp.route('/clinica/<string:clinica_id>/medico', methods=['PUT'])
@inject
def update_medico_clinica(clinica_id, medico_usecase: ClinicaUseCase):
    try:
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return jsonify({'message': 'Clínica não encontrada'}), 404
        data = request.json
        result = medico_usecase.update_medico(clinica, data)

        if result == -1:
            return jsonify({'message': 'Medico não encontrada'}), 404
        if result == 0:
            return jsonify({'message': 'Médico já está associado a clínica', 'result': result}), 200
      
        return jsonify({'message': 'Médico adicionado à clínica com sucesso', 'result': result}), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao atualizar o médico', 'error': str(e)}), 400
    