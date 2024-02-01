from flask import request, jsonify
from datetime import datetime, timedelta
import jwt 
from functools import wraps
from dotenv import load_dotenv
import os
load_dotenv()

# Função para gerar um token de acesso
def generate_access_token(data):
    payload = {
        'exp': (datetime.utcnow() + timedelta(days=3)).timestamp(),  # Expiração em 1 dia
        'sub': data
    } 
    access_token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return access_token

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
