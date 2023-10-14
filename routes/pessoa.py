from flask import Blueprint, request, jsonify
from models import Pessoa,db

pessoa_bp = Blueprint('pessoa', __name__, url_prefix='/pessoa')

# Rota para criar um novo registro
@pessoa_bp.route('/pessoa', methods=['POST'])
def create_pessoa():
    try:
        data = request.json
        nova_pessoa = Pessoa(**data)
        db.session.add(nova_pessoa)
        db.session.commit()
        return jsonify({'message': 'Pessoa criada com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@pessoa_bp.route('/pessoa', methods=['GET'])
def get_pessoas():
    # Obtenha os parâmetros de consulta da URL
    nome = request.args.get('nome')
    cpf = request.args.get('cpf')
    id = request.args.get('id')
    data_nascimento = request.args.get('data_nascimento')
    telefone = request.args.get('telefone')
    cargo = request.args.get('cargo')

    # Consulta inicial para todas as pessoas
    query = Pessoa.query

    # Filtre a consulta com base nos parâmetros de consulta
    if nome:
        query = query.filter(Pessoa.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(Pessoa.cpf == cpf)
    if id:
        query = query.filter(Pessoa.id == id)
    if data_nascimento:
        query = query.filter(Pessoa.data_nascimento == data_nascimento)
    if telefone:
        query = query.filter(Pessoa.telefone == telefone)
    if cargo:
        query = query.filter(Pessoa.cargo.ilike(f"%{cargo}%"))

    # Execute a consulta
    pessoas = query.all()

    # Converta os resultados em um formato JSON
    pessoas_list = []
    for pessoa in pessoas:
        pessoas_list.append({
            'id': pessoa.id,
            'cpf': pessoa.cpf,
            'data_nascimento': str(pessoa.data_nascimento),
            'nome': pessoa.nome,
            'telefone': pessoa.telefone,
            'cargo': pessoa.cargo
        })

    return jsonify(pessoas_list)

# Rota para atualizar os dados de uma pessoa
@pessoa_bp.route('/pessoa/<string:pessoa_id>', methods=['PUT'])
def update_pessoa(pessoa_id):
    try:
        data = request.json
        pessoa = Pessoa.query.get(pessoa_id)
        if not pessoa:
            return jsonify({'error': 'Pessoa não encontrada'}), 404
        for key, value in data.items():
            setattr(pessoa, key, value)
        db.session.commit()
        return jsonify({'message': 'Dados da pessoa atualizados com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para excluir uma pessoa
@pessoa_bp.route('/pessoa/<string:pessoa_id>', methods=['DELETE'])
def delete_pessoa(pessoa_id):
    try:
        pessoa = Pessoa.query.get(pessoa_id)
        if not pessoa:
            return jsonify({'error': 'Pessoa não encontrada'}), 404
        db.session.delete(pessoa)
        db.session.commit()
        return jsonify({'message': 'Pessoa excluída com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
