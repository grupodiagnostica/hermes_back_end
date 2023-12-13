from flask import Blueprint, request, jsonify
from models import db, Diagnostico
from datetime import datetime
from routes.medico import token_required

diagnostico_bp = Blueprint('diagnostico', __name__)

# Rota para criar um novo diagnóstico
@diagnostico_bp.route('/diagnostico', methods=['POST'])
@token_required
def create_diagnostico():
    try:
        data = request.json
        novo_diagnostico = Diagnostico(**data)
        db.session.add(novo_diagnostico)
        db.session.commit() 
        novo_diagnostico_json={
           'id' : novo_diagnostico.id,
           'modelo' : novo_diagnostico.modelo,
           'id_medico' : novo_diagnostico.id_medico,
           'data_hora' : novo_diagnostico.data_hora,
           'id_paciente' : novo_diagnostico.id_paciente,
           'resultado' : novo_diagnostico.resultado,
           'laudo_medico' : novo_diagnostico.laudo_medico,
           'mapa_calor': novo_diagnostico.mapa_calor,
            'resultado_modelo': novo_diagnostico.resultado_modelo,
            'resultado_real': novo_diagnostico.resultado_real,
        }
               
        return jsonify({'data': novo_diagnostico_json}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

# Rota para obter diagnósticos com filtros
@diagnostico_bp.route('/diagnostico', methods=['GET'])
@token_required
def get_diagnosticos():
    # Obtenha os parâmetros de consulta da URL
    id = request.args.get('id')
    id_medico = request.args.get('id_medico')
    id_paciente = request.args.get('id_paciente')

    # Consulta inicial para todos os diagnósticos
    query = Diagnostico.query

    # Filtre a consulta com base nos parâmetros de consulta
    if id:
        query = query.filter(Diagnostico.id == id)
    if id_medico:
        query = query.filter(Diagnostico.id_medico == id_medico)
    if id_paciente:
        query = query.filter(Diagnostico.id_paciente == id_paciente)

    # Execute a consulta
    diagnosticos = query.all()

    # Converta os resultados em um formato JSON
    diagnosticos_list = []
    for diagnostico in diagnosticos:
        diagnosticos_list.append({
            'id': diagnostico.id,
            'modelo': diagnostico.modelo,
            'id_medico': diagnostico.id_medico,
            'data_hora': str(diagnostico.data_hora),
            'raio_x': diagnostico.raio_x,
            'id_paciente': diagnostico.id_paciente,
            'resultado': diagnostico.resultado,
            'laudo_medico': diagnostico.laudo_medico,
            'mapa_calor': diagnostico.mapa_calor,
            'resultado_modelo': diagnostico.resultado_modelo,
            'resultado_real': diagnostico.resultado_real,
        })

    return jsonify(diagnosticos_list)

# Rota para atualizar os dados de um diagnóstico
@diagnostico_bp.route('/diagnostico/<int:diagnostico_id>', methods=['PUT'])
@token_required
def update_diagnostico(diagnostico_id):
    try:
        data = request.json
        diagnostico = Diagnostico.query.get(diagnostico_id)
        if not diagnostico:
            return jsonify({'error': 'Diagnóstico não encontrado'}), 404
        for key, value in data.items():
            setattr(diagnostico, key, value)
        db.session.commit()
        return jsonify({'message': 'Dados do diagnóstico atualizados com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para excluir um diagnóstico
@diagnostico_bp.route('/diagnostico/<int:diagnostico_id>', methods=['DELETE'])
@token_required
def delete_diagnostico(diagnostico_id):
    try:
        diagnostico = Diagnostico.query.get(diagnostico_id)
        if not diagnostico:
            return jsonify({'error': 'Diagnóstico não encontrado'}), 404
        db.session.delete(diagnostico)
        db.session.commit()
        return jsonify({'message': 'Diagnóstico excluído com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
