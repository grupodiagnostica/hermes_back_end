# controllers/medico_controller.py
from flask import Blueprint, request, jsonify
from usecases.medico import MedicoUseCase

medico_bp = Blueprint('medico', __name__)
medico_usecase = MedicoUseCase()

@medico_bp.route('/medico', methods=['POST'])
def create_medico():
    try:
        data = request.json
        novo_medico = medico_usecase.create_medico(data)
        return jsonify({'data': novo_medico}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@medico_bp.route('/medico', methods=['GET'])
def get_medicos():
    try:
        id_pessoa = request.args.get('id_pessoa')
        crm = request.args.get('crm')
        especialidade = request.args.get('especialidade')
        medicos_list = medico_usecase.get_medicos(id_pessoa, crm, especialidade)
        return jsonify({'data': medicos_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@medico_bp.route('/medico/<string:medico_id>', methods=['PUT'])
def update_medico(medico_id):
    try:
        data = request.json
        medico_atualizado = medico_usecase.update_medico(medico_id, data)
        return jsonify({'data': medico_atualizado}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@medico_bp.route('/medico/<string:medico_id>', methods=['DELETE'])
def delete_medico(medico_id):
    try:
        medico_usecase.delete_medico(medico_id)
        return jsonify({'message': 'Médico excluído com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@medico_bp.route('/medico/<string:medico_id>/clinica', methods=['GET'])
def get_clinicas_medico(medico_id):
    try:
        clinicas_list = medico_usecase.get_clinicas_medico(medico_id)
        return jsonify({"data": clinicas_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@medico_bp.route('/medico/<string:medico_crm>', methods=['POST'])
def existe_medico(medico_crm):
    try:
        existe = medico_usecase.existe_medico(medico_crm)
        return jsonify({'result': existe}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
