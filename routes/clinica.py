from flask import Blueprint, request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from models import Clinica, Medico
from models import db
from routes.login import token_required

clinica_bp = Blueprint('clinica', __name__)

# Rota para criar uma nova clínica
@clinica_bp.route('/clinica', methods=['POST'])
def create_clinica():
    try:
        data = request.json
        senha_criptografada = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        data['senha'] = senha_criptografada.decode('utf-8')
        nova_clinica = Clinica(**data)
        db.session.add(nova_clinica)
        db.session.commit()
        return jsonify({'message': 'Clínica criada com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@clinica_bp.route('/clinica', methods=['GET'])
@token_required
def get_clinicas():
    # Obtenha os parâmetros de consulta da URL
    cnpj = request.args.get('cnpj')
    nome = request.args.get('nome')

    # Consulta inicial para todas as clínicas
    query = Clinica.query

    # Filtre a consulta com base nos parâmetros de consulta
    if cnpj:
        query = query.filter(Clinica.cnpj == cnpj)
    if nome:
        query = query.filter(Clinica.nome.ilike(f"%{nome}%"))

    # Execute a consulta
    clinicas = query.all()

    # Converta os resultados em um formato JSON
    clinicas_list = []
    for clinica in clinicas:
        clinicas_list.append({
            'id': clinica.id,
            'cnpj': clinica.cnpj,
            'nome': clinica.nome
        })

    return jsonify(clinicas_list)


# Rota para atualizar os dados de uma clínica
@clinica_bp.route('/clinica/<string:clinica_id>', methods=['PUT'])
@token_required
def update_clinica(clinica_id):
    try:
        data = request.json
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return jsonify({'error': 'Clínica não encontrada'}), 404
        for key, value in data.items():
            setattr(clinica, key, value)
        db.session.commit()
        return jsonify({'message': 'Dados da clínica atualizados com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para excluir uma clínica
@clinica_bp.route('/clinica/<string:clinica_id>', methods=['DELETE'])
@token_required
def delete_clinica(clinica_id):
    try:
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return jsonify({'error': 'Clínica não encontrada'}), 404
        db.session.delete(clinica)
        db.session.commit()
        return jsonify({'message': 'Clínica excluída com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@clinica_bp.route('/clinica/<string:clinica_id>/adicionar_medico', methods=['POST'])
def adicionar_medico_a_clinica(clinica_id):
    # Verifica se a clínica existe
    clinica = Clinica.query.get(clinica_id)
    if not clinica:
        return jsonify({'mensagem': 'Clínica não encontrada'}), 404

    # Obtém dados do médico a partir do corpo da requisição
    dados_medico = request.get_json()

    # Cria um novo objeto Medico
    novo_medico = Medico(
        id_pessoa=dados_medico['id_pessoa'],
        crm=dados_medico['crm'],
        especialidade=dados_medico['especialidade'],
        senha=dados_medico['senha'],
        email=dados_medico['email'],
        foto_perfil=dados_medico.get('foto_perfil')  # Pode ser None
    )

    # Adiciona o médico à clínica
    clinica.medicos.append(novo_medico)

    # Commit no banco de dados
    db.session.commit()

    return jsonify({'mensagem': 'Médico adicionado à clínica com sucesso'})
