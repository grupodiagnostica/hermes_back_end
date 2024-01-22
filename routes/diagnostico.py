from flask import Blueprint, request, jsonify
from models import db, Diagnostico
from datetime import datetime
from routes.login import token_required

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
        novo_diagnostico_json = {
           'id' : novo_diagnostico.id,
           'modelo' : novo_diagnostico.modelo,
           'id_medico' : novo_diagnostico.id_medico,
           'id_clinica': novo_diagnostico.id_clinica,
           'data_hora' : novo_diagnostico.data_hora,
           'id_paciente' : novo_diagnostico.id_paciente,
           'laudo_medico' : novo_diagnostico.laudo_medico,
            'raio_x': novo_diagnostico.raio_x,
           'mapa_calor': novo_diagnostico.mapa_calor,
            'resultado_modelo': novo_diagnostico.resultado_modelo,
            'resultado_real': novo_diagnostico.resultado_real,
            'paciente': {
            'id': novo_diagnostico.paciente.id,
            'id_pessoa': novo_diagnostico.paciente.id_pessoa,
            'sexo': novo_diagnostico.paciente.sexo,
            'tipo_sanguineo': novo_diagnostico.paciente.tipo_sanguineo,
            'cidade': novo_diagnostico.paciente.cidade,
            'estado': novo_diagnostico.paciente.estado,
            'numero': novo_diagnostico.paciente.numero,
            'logradouro': novo_diagnostico.paciente.logradouro,
            'bairro': novo_diagnostico.paciente.bairro,
            'detalhes_clinicos': novo_diagnostico.paciente.detalhes_clinicos,
            'pessoa': {
                'id': novo_diagnostico.paciente.pessoa.id,
                'cpf': novo_diagnostico.paciente.pessoa.cpf,
                'data_nascimento': str(novo_diagnostico.paciente.pessoa.data_nascimento),
                'nome': novo_diagnostico.paciente.pessoa.nome,
                'telefone': novo_diagnostico.paciente.pessoa.telefone,
                'cargo': novo_diagnostico.paciente.pessoa.cargo
            }
            }
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
