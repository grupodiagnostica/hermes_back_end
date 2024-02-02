from flask import Blueprint, request, jsonify
from models import db, Modelo
from routes.login import token_required
modelo_bp = Blueprint('modelo', __name__)

# Rota para criar um novo modelo
@modelo_bp.route('/modelo', methods=['POST'])
@token_required
def create_modelo():
    try:
        data = request.json
        novo_modelo = Modelo(**data)
        db.session.add(novo_modelo)
        db.session.commit()
        return jsonify({'message': 'Modelo criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para obter modelos com filtros
@modelo_bp.route('/modelo', methods=['GET'])
@token_required
def get_modelos():
    try:
        # Obtenha os parâmetros de consulta da URL
        id = request.args.get('id')
        nome = request.args.get('nome')
        cnpj = request.args.get('cnpj')

        # Consulta inicial para todos os modelos
        query = Modelo.query

        # Filtre a consulta com base nos parâmetros de consulta
        if id:
            query = query.filter(Modelo.id == id)
        if nome:
            query = query.filter(Modelo.nome.ilike(f"%{nome}%"))
        if cnpj:
            query = query.filter(Modelo.cnpj == cnpj)

        # Execute a consulta
        modelos = query.all()

        # Converta os resultados em um formato JSON
        modelos_list = []
        for modelo in modelos:
            modelos_list.append({
                'id': modelo.id,
                'nome': modelo.nome,
                'precisao': modelo.precisao,
                'acuracia': modelo.acuracia,
                'f1score': modelo.f1score,
                'recall': modelo.recall,
                'kappa': modelo.kappa,
                'filtros': modelo.filtros,
                'data_augmentation': modelo.data_augmentation,
                'data_hora': modelo.data_hora,
                'cnpj':modelo.cnpj
            })
        return jsonify({'data': modelos_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400



# Rota para atualizar os dados de um modelo
@modelo_bp.route('/modelo/<string:modelo_id>', methods=['PUT'])
@token_required
def update_modelo(modelo_id):
    try:
        data = request.json
        modelo = Modelo.query.get(modelo_id)
        if not modelo:
            return jsonify({'error': 'Modelo não encontrado'}), 404
        for key, value in data.items():
            setattr(modelo, key, value)
        db.session.commit()
        return jsonify({'message': 'Dados do modelo atualizados com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para excluir um modelo
@modelo_bp.route('/modelo/<string:modelo_id>', methods=['DELETE'])
@token_required
def delete_modelo(modelo_id):
    try:
        modelo = Modelo.query.get(modelo_id)
        if not modelo:
            return jsonify({'error': 'Modelo não encontrado'}), 404
        db.session.delete(modelo)
        db.session.commit()
        return jsonify({'message': 'Modelo excluído com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
