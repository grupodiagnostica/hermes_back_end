from datetime import datetime, timedelta
import jwt 
import os

# Função para gerar um token de acesso
def generate_access_token(data):
    payload = {
        'exp': (datetime.utcnow() + timedelta(days=3)).timestamp(), 
        'sub': data
    } 
    access_token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return access_token