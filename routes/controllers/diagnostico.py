# controllers.py
from flask import jsonify, Blueprint, request
from injector import inject
from routes.middleware.token import token_required
from usecases import DiagnosticoUseCase

diagnostico_bp = Blueprint('diagnostico', __name__)

@diagnostico_bp.route('/diagnostico', methods=['POST'])
@token_required
@inject
def create_diagnostico(diagnostico_usecase: DiagnosticoUseCase):
    try:
        data = request.json
        novo_diagnostico = diagnostico_usecase.create_diagnostico(data)
        # ... (formato da resposta JSON)
        return jsonify({'data': novo_diagnostico}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

@diagnostico_bp.route('/diagnostico', methods=['GET'])
@token_required
@inject
def get_diagnosticos(diagnostico_usecase: DiagnosticoUseCase):
    try:
        
        id = request.args.get('id')
        id_medico = request.args.get('id_medico')
        id_clinica = request.args.get('id_clinica')
        id_paciente = request.args.get('id_paciente')

        diagnosticos_list = diagnostico_usecase.get_diagnosticos(id, id_medico, id_clinica, id_paciente)

        return jsonify(diagnosticos_list)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400
    
@diagnostico_bp.route('/diagnostico/<int:diagnostico_id>', methods=['PUT'])
@token_required
@inject
def update_diagnostico(diagnostico_id, diagnostico_usecase: DiagnosticoUseCase):
    try:
        data = request.json
        diagnostico_atualizado = diagnostico_usecase.update_diagnostico(diagnostico_id, data)
        if diagnostico_atualizado:
            return jsonify({'message': 'Dados do diagnóstico atualizados com sucesso', 'data': diagnostico_atualizado}), 200
        else:
            return jsonify({'error': 'Diagnóstico não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@diagnostico_bp.route('/diagnostico/<int:diagnostico_id>', methods=['DELETE'])
@token_required
@inject
def delete_diagnostico(diagnostico_id, diagnostico_usecase: DiagnosticoUseCase):
    try:
        sucesso = diagnostico_usecase.delete_diagnostico(diagnostico_id)
        if sucesso:
            return jsonify({'message': 'Diagnóstico excluído com sucesso'}), 200
        else:
            return jsonify({'error': 'Diagnóstico não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@diagnostico_bp.route('/diagnostico/atendimentos/<int:anoRef>', methods=['POST'])
@token_required
@inject
def diagnostico_atendimentos(anoRef, diagnostico_usecase: DiagnosticoUseCase):
    try:
        args = request.json 
        atendimentos = diagnostico_usecase.get_atendimentos_por_ano(args['clinica_id'], anoRef)
        if atendimentos == 0:
            return jsonify({'message': 'Não existem atendimentos', 'result': 0}), 200
        # Formatando a resposta JSON
        return jsonify({'result': 1, 'labels': atendimentos['labels'], 'data': atendimentos['data']}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

@diagnostico_bp.route('/diagnostico/classificacoes/<string:modelo>', methods=['POST'])
@token_required
@inject
def diagnostico_classificacoes( diagnostico_usecase: DiagnosticoUseCase):
    try:
        args = request.json
        classificacoes = diagnostico_usecase.diagnostico_classificacoes(args['clinica_id'])
        if classificacoes == 0:
            return jsonify({'message': 'Não existem diagnósticos', 'result': 0}), 200
        # Formatando a resposta JSON
        return jsonify({'result': 1, 'labels': classificacoes['labels'], 'data': classificacoes['data']}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

@diagnostico_bp.route('/diagnostico/diagnosticos/<int:anoRef>', methods=['POST'])
@token_required
@inject
def diagnostico_diagnosticos(anoRef, diagnostico_usecase: DiagnosticoUseCase):
    try:
        args = request.json
        diagnosticos = diagnostico_usecase.get_diagnosticos_por_ano(args['clinica_id'], anoRef)
        if diagnosticos == 0:
            return jsonify({'message': 'Não existem diagnósticos', 'result': 0}), 200
        # Formatando a resposta JSON
        return jsonify({'result': 1, 'labels': diagnosticos['labels'], 'lines': diagnosticos['lines'], 'data': diagnosticos['data']}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

@diagnostico_bp.route('/diagnostico/diagnosticos/classificacoes', methods=['POST'])
@token_required
@inject
def diagnostico_diagnosticos_classificacoes(diagnostico_usecase: DiagnosticoUseCase):
    try:
        args = request.json
        comparacoes = diagnostico_usecase.get_comparacoes_diagnosticos_classificacoes(args['clinica_id'])
        if not comparacoes:
            return jsonify({'message': 'Não existem diagnósticos', 'result': 0}), 200
        # Formatando a resposta JSON
        return jsonify({'result': 1, 'labels': comparacoes['labels'], 'classes': comparacoes['classes'], 'data': comparacoes['data']}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400
