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
        # Obtenha os parâmetros de consulta da URL
        id = request.args.get('id')
        id_medico = request.args.get('id_medico')
        id_clinica = request.args.get('id_clinica')
        id_paciente = request.args.get('id_paciente')

        # Use o caso de uso para obter os diagnósticos
        diagnosticos = diagnostico_usecase.get_diagnosticos(id, id_medico, id_clinica, id_paciente)

        # Converta os resultados em um formato JSON
        diagnosticos_list = []
        for diagnostico in diagnosticos:
            # ... (formato da resposta JSON)
           diagnosticos_list.append({
            'id': diagnostico.id,
            'modelo': diagnostico.modelo,
            'id_medico': diagnostico.id_medico,
            'id_clinica' : diagnostico.id_clinica,
            'data_hora': str(diagnostico.data_hora),
            'raio_x': diagnostico.raio_x,
            'id_paciente': diagnostico.id_paciente,
            'laudo_medico': diagnostico.laudo_medico,
            'mapa_calor': diagnostico.mapa_calor,
            'resultado_modelo': diagnostico.resultado_modelo,
            'resultado_real': diagnostico.resultado_real,
            'paciente': {
            'id': diagnostico.paciente.id,
            'id_pessoa': diagnostico.paciente.id_pessoa,
            'sexo': diagnostico.paciente.sexo,
            'tipo_sanguineo': diagnostico.paciente.tipo_sanguineo,
            'cidade': diagnostico.paciente.cidade,
            'estado': diagnostico.paciente.estado,
            'numero': diagnostico.paciente.numero,
            'logradouro': diagnostico.paciente.logradouro,
            'bairro': diagnostico.paciente.bairro,
            'detalhes_clinicos': diagnostico.paciente.detalhes_clinicos,
            'pessoa': {
                'id': diagnostico.paciente.pessoa.id,
                'cpf': diagnostico.paciente.pessoa.cpf,
                'data_nascimento': str(diagnostico.paciente.pessoa.data_nascimento),
                'nome': diagnostico.paciente.pessoa.nome,
                'telefone': diagnostico.paciente.pessoa.telefone,
                'cargo': diagnostico.paciente.pessoa.cargo
            }
            }
        })

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
