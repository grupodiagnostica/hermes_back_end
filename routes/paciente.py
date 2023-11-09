from flask import Blueprint, request, jsonify
from models import Paciente,db

paciente_bp = Blueprint('paciente', __name__)

# Rota para criar um novo registro
@paciente_bp.route('/paciente', methods=['POST'])
def create_paciente():
    try:
        data = request.json
        novo_paciente = Paciente(**data)
        db.session.add(novo_paciente)
        db.session.commit()
        return jsonify({'message': 'Paciente criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para obter pacientes
@paciente_bp.route('/paciente', methods=['GET'])
def get_pacientes():
    # Obtenha os parâmetros de consulta da URL
    id_pessoa = request.args.get('id_pessoa')
    sexo = request.args.get('sexo')
    tipo_sanguineo = request.args.get('tipo_sanguineo')
    cidade = request.args.get('cidade')
    estado = request.args.get('estado')

    # Consulta inicial para todos os pacientes
    query = Paciente.query

    # Filtre a consulta com base nos parâmetros de consulta
    if id_pessoa:
        query = query.filter(Paciente.id_pessoa == id_pessoa)
    if sexo:
        query = query.filter(Paciente.sexo == sexo)
    if tipo_sanguineo:
        query = query.filter(Paciente.tipo_sanguineo == tipo_sanguineo)
    if cidade:
        query = query.filter(Paciente.cidade == cidade)
    if estado:
        query = query.filter(Paciente.estado == estado)

    # Execute a consulta
    pacientes = query.all()

    # Converta os resultados em um formato JSON
    pacientes_list = []
    for paciente in pacientes:
        pacientes_list.append({
            'id': paciente.id,
            'id_pessoa': paciente.id_pessoa,
            'sexo': paciente.sexo,
            'tipo_sanguineo': paciente.tipo_sanguineo,
            'cidade': paciente.cidade,
            'estado': paciente.estado
        })

    return jsonify(pacientes_list)

# Rota para atualizar os dados de um paciente
@paciente_bp.route('/paciente/<string:paciente_id>', methods=['PUT'])
def update_paciente(paciente_id):
    try:
        data = request.json
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        for key, value in data.items():
            setattr(paciente, key, value)
        db.session.commit()
        return jsonify({'message': 'Dados do paciente atualizados com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para excluir um paciente
@paciente_bp.route('/paciente/<string:paciente_id>', methods=['DELETE'])
def delete_paciente(paciente_id):
    try:
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'message': 'Paciente excluído com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400