from flask import request, jsonify
from functools import wraps
import jwt 
import os

# Função para verificar se o token é válido
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            print('Token ausente')
            return jsonify({'error': 'Token ausente'}), 401
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            print('Token expirado')
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            print('Token inválido')
            return jsonify({'error': 'Token inválido'}), 401

        return f(*args, **kwargs)

    return decorated