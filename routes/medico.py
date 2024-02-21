from flask import Blueprint, request, jsonify
from models import db, Medico
import bcrypt
from routes.login import token_required
from dotenv import load_dotenv
load_dotenv()



medico_bp = Blueprint('medico', __name__)


# Rota para criar um novo médico
@medico_bp.route('/medico', methods=['POST'])
def create_medico():
    try:
        data = request.json
        # Criptografa a senha
        senha_criptografada = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        data['senha'] = senha_criptografada.decode('utf-8')
        novo_medico =  Medico(**data)
        db.session.add(novo_medico)
        db.session.commit()
        medicoJson = {
            'id': novo_medico.id,
            'id_pessoa': novo_medico.id_pessoa,
            'crm': novo_medico.crm,
            'especialidade': novo_medico.especialidade,
            'senha': novo_medico.senha,
            'email' : novo_medico.email,
            'foto_perfil': novo_medico.foto_perfil,
            'pessoa': {
                'id': novo_medico.pessoa.id,
                'cpf': novo_medico.pessoa.cpf,
                'data_nascimento': str(novo_medico.pessoa.data_nascimento),
                'nome': novo_medico.pessoa.nome,
                'telefone': novo_medico.pessoa.telefone,
                'cargo': novo_medico.pessoa.cargo
            }
        }
        return jsonify({'data': medicoJson}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@medico_bp.route('/medico', methods=['GET'])
@token_required
def get_medicos():
    # Obtenha os parâmetros de consulta da URL
    id_pessoa = request.args.get('id_pessoa')
    crm = request.args.get('crm')
    especialidade = request.args.get('especialidade')


    # Consulta inicial para todos os médicos
    query = Medico.query

    # Filtre a consulta com base nos parâmetros de consulta
    if id_pessoa:
        query = query.filter(Medico.id_pessoa == id_pessoa)
    if crm:
        query = query.filter(Medico.crm == crm)
    if especialidade:
        query = query.filter(Medico.especialidade == especialidade)

    # Execute a consulta
    medicos = query.all()

    # Converta os resultados em um formato JSON
    medicos_list = [{
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
            }}for medico in medicos ]

    return jsonify(medicos_list)

# Rota para saber as clínicas associadas a um médico
@medico_bp.route('/medico/<string:medico_id>/clinica', methods=['GET'])
def get_clinicas_medico(medico_id):
    medico = Medico.query.get(medico_id)

    if medico:
        clinicas = medico.clinicas
        clinicasJson = [{
            'id': clinica.id,
            'cep': clinica.cep,
            'cnpj': clinica.cnpj,
            'email' : clinica.email,
            'nome' : clinica.nome,
            'foto_perfil': clinica.foto_perfil,
            'modelo_id': clinica.modelo_id, 
        } for clinica in clinicas]
        return jsonify({"data":clinicasJson})
    else:
        return jsonify({"mensagem": "Clínica não encontrada"}), 404




# @medico_bp.route('/medico/login', methods=['POST'])
# def login_medico():
#     data = request.json

#     # Consulta inicial para todos os médicos
#     query = Medico.query

#     # Filtre a consulta com base nos parâmetros de consulta
#     if data.email:
#         query = query.filter(Medico.email == data.email)

#     # Execute a consulta
#     medicos = query.all()

#     # Converta os resultados em um formato JSON
#     medicos_list = []
#     for medico in medicos:
#         medicos_list.append({
#             'id': medico.id,
#             'id_pessoa': medico.id_pessoa,
#             'crm': medico.crm,
#             'email': medico.email,
#             'senha': medico.senha,
#             'especialidade': medico.especialidade,
#                'pessoa': {
#                 'id': medico.pessoa.id,
#                 'cpf': medico.pessoa.cpf,
#                 'data_nascimento': str(medico.pessoa.data_nascimento),
#                 'nome': medico.pessoa.nome,
#                 'telefone': medico.pessoa.telefone,
#                 'cargo': medico.pessoa.cargo
#             }
#         })

#     medico = medicos_list[0]

#     if bcrypt.checkpw(data.senha.encode('utf-8'), medico.senha):
#         return jsonify(medico)
#     else:
#         return jsonify({'error': "Email ou senha incorretos"}), 401

# Rota para atualizar os dados de um médico
@medico_bp.route('/medico/<string:medico_id>', methods=['PUT'])
@token_required
def update_medico(medico_id):
    try:
        data = request.json
        medico = Medico.query.get(medico_id)
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404
        for key, value in data.items():
            setattr(medico, key, value)
        db.session.commit()

        medicoJson = {
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
        }
        return jsonify({'data': medicoJson})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

# Rota para excluir um médico
@medico_bp.route('/<string:medico_id>', methods=['DELETE'])
@token_required
def delete_medico(medico_id):
    try:
        medico = Medico.query.get(medico_id)
        if not medico:
            return jsonify({'error': 'Médico não encontrado'}), 404
        db.session.delete(medico)
        db.session.commit()
        return jsonify({'message': 'Médico excluído com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# Rota para saber se uma médico já existe pelo crm
@medico_bp.route('/medico/<string:medico_crm>', methods=['POST'])
@token_required
def existe_medico(medico_crm):
    try:
        medico = Medico.query.filter(Medico.crm == medico_crm).first()
        if medico:
            medicoJson = {
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
            }
            return jsonify({'result': 1, 'data': medicoJson}), 200
        return jsonify({'result': 0}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
