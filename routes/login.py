from flask import Blueprint, request, jsonify
from models import db, Medico, Clinica, Administrador
import bcrypt
from datetime import datetime, timedelta
import jwt 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from functools import wraps
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
load_dotenv()

login_bp = Blueprint('login', __name__)

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

# Rota para fazer login
@login_bp.route('/login', methods=['POST'])
def login_medico_clinica():
    try:
        data = request.json
        senha = data['senha']
            
        email = data['email']
        medico = Medico.query.filter_by(email=email).first()
        if medico: 
            if bcrypt.checkpw(senha.encode('utf-8'), medico.senha.encode('utf-8')):
                access_token = generate_access_token(medico.email)
                medicoJson = {
                'id': medico.id,
                'id_pessoa': medico.id_pessoa,
                'crm': medico.crm,
                'especialidade': medico.especialidade,
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
                return jsonify({'token': access_token, 'data': medicoJson})  
            else:
                return jsonify({'error': 'Email ou senha incorretos'}), 401
            
        clinica = Clinica.query.filter_by(email=email).first()
        if clinica:
            if bcrypt.checkpw(senha.encode('utf-8'), clinica.senha.encode('utf-8')):
                access_token = generate_access_token(clinica.cnpj)
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
                }
                return jsonify({'token': access_token,
                                'data': clinicaJson})  
            else:
                return jsonify({'error': 'CNPJ ou senha incorretos'}), 401
            
        if data['username']:
            username = data['username']
            administrador = Administrador.query.filter_by(username=username).first()

            if administrador and bcrypt.checkpw(senha.encode('utf-8'), administrador.senha.encode('utf-8')):
                # Gerar um token de autenticação
                access_token = generate_access_token(administrador.username)
                administradorJson = {
                'id': administrador.id,
                'username' : administrador.username,
                }
                return jsonify({'token': access_token,
                                'data': administradorJson}) 
    except Exception as e:
        print(e)
        print("123")
        return jsonify({'error': str(e)}), 400
    