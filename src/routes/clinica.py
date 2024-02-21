from flask import Blueprint, request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from models import Clinica, Medico
from models import db
from src.middleware.token import token_required

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
    cnpj = request.args.get('cnpj')
    nome = request.args.get('nome')

    query = Clinica.query

    if cnpj:
        query = query.filter(Clinica.cnpj == cnpj)
    if nome:
        query = query.filter(Clinica.nome.ilike(f"%{nome}%"))

    clinicas = query.all()

    clinicas_list = []
    for clinica in clinicas:
        clinicas_list.append({
            'id': clinica.id,
            'cnpj': clinica.cnpj,
            'nome': clinica.nome,
            'modelo_id': clinica.modelo_id,
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
        clinicaJson = {
                'id': clinica.id,
                'cnpj': clinica.cnpj,
                'nome': clinica.nome,
                'foto_perfil': clinica.foto_perfil,
                'cidade': clinica.cidade,
                'estado': clinica.estado,
                'telefone': clinica.telefone,
                'numero': clinica.numero,
                'cep': clinica.cep,
                'logradouro': clinica.logradouro,
                'bairro': clinica.bairro,
                'email': clinica.email,
                'modelo_id': clinica.modelo_id,
        }
        return jsonify({'data': clinicaJson})
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
    
@clinica_bp.route('/clinica/<string:clinica_id>/medico', methods=['POST'])
def create_medico_clinica(clinica_id):
    try:
        clinica = Clinica.query.get(clinica_id)
        if not clinica:
            return jsonify({'message': 'Clínica não encontrada'}), 404

        data = request.json
        senha_criptografada = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        data['senha'] = senha_criptografada.decode('utf-8')
        novo_medico =  Medico(**data)
        novo_medico.clinicas.append(clinica)
        db.session.add(novo_medico)
        db.session.commit()

        return jsonify({'message': 'Médico adicionado à clínica com sucesso'})  
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao criar o médico'})  
    

@clinica_bp.route('/clinica/<string:clinica_id>/medico', methods=['GET'])
def get_medicos_clinica(clinica_id):
    clinica = Clinica.query.get(clinica_id)

    if clinica:
        medicos = clinica.medicos
        medicosJson = [{
            'id': medico.id,
            'id_pessoa': medico.id_pessoa,
            'crm': medico.crm,
            'especialidade': medico.especialidade,
            'senha': medico.senha,
            'email' : medico.email,
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
        return jsonify({"data":medicosJson})
    else:
        return jsonify({"mensagem": "Clínica não encontrada"}), 404

@clinica_bp.route('/clinica/<string:clinica_id>/medico', methods=['PUT'])
def update_medico_clinica(clinica_id):
    try:
        clinica = Clinica.query.get(clinica_id)

        if not clinica:
            return jsonify({'message': 'Clínica não encontrada'}), 404

        data = request.json
        medico = Medico.query.filter(Medico.crm == data['crm']).first()

        if not medico:
            return jsonify({'message': 'Medico não encontrada'}), 404
        if clinica in medico.clinicas:
            return jsonify({'message': 'Médico já está associado a clínica', 'result': 0}), 200
    
        medico.clinicas.append(clinica)
        db.session.commit()
        return jsonify({'message': 'Médico adicionado à clínica com sucesso', 'result': 1}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao criar o médico'}), 200
