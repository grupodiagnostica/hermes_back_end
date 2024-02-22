from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from models import StatusRequisicao, db, Requisicao
from src.middleware.token import token_required
requisicao_bp = Blueprint('requisicao', __name__)

# Rota para criar um novo requisicao
@requisicao_bp.route('/requisicao', methods=['POST'])
@token_required
def create_requisicao():
    try:
        data = request.json
        novo_requisicao = Requisicao(**data)
        db.session.add(novo_requisicao)
        db.session.commit()
        return jsonify({'message': 'requisicao criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@requisicao_bp.route('/requisicao', methods=['GET'])
@token_required
def get_requisicaos():
    try:
        id = request.args.get('id')
        id_clinica = request.args.get('id_clinica')
        status = request.args.get('status')

        query = Requisicao.query

        if id:
            query = query.filter(Requisicao.id == id)
        if id_clinica:
            query = query.filter(Requisicao.id_clinica == id_clinica)
        if status and status.upper() in [s.value for s in StatusRequisicao]:
            query = query.filter(Requisicao.status == StatusRequisicao[status.upper()])

        query = query.order_by(desc(Requisicao.data_hora))
        requisicaos = query.all()

        requisicaos_list = []
        for requisicao in requisicaos:
            requisicaos_list.append({
                'id': requisicao.id,
                'quantidade_imagens': requisicao.quantidade_imagens,
                'id_clinica': requisicao.id_clinica,
                'data_hora': requisicao.data_hora ,
                'status': requisicao.status.value  
            })
        return jsonify({'data': requisicaos_list}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400




# Rota para atualizar os dados de um requisicao
@requisicao_bp.route('/requisicao/<string:requisicao_id>', methods=['PUT'])
@token_required
def update_requisicao(requisicao_id):
    try:
        data = request.json
        requisicao = Requisicao.query.get(requisicao_id)
        if not requisicao:
            return jsonify({'error': 'requisicao não encontrado'}), 404
        setattr(requisicao, 'status', data['status'])
        db.session.commit()
        return jsonify({'message': 'Dados do requisicao atualizados com sucesso'})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

# Rota para excluir um requisicao
@requisicao_bp.route('/requisicao/<string:requisicao_id>', methods=['DELETE'])
@token_required
def delete_requisicao(requisicao_id):
    try:
        requisicao = Requisicao.query.get(requisicao_id)
        if not requisicao:
            return jsonify({'error': 'requisicao não encontrado'}), 404
        db.session.delete(requisicao)
        db.session.commit()
        return jsonify({'message': 'requisicao excluído com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
