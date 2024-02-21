import smtplib
import email.message
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from flask import Blueprint,request ,jsonify
import math
email_bp = Blueprint('email', __name__)
import random


@email_bp.route('/email/recuperar-senha', methods=['POST'])
def recuperar_senha():
    try:
        data = request.json
        codigo = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        corpo_email = f"""
        <p>Email para recuperação de senha</p>
        <p>Seu codigo é:</p>
        <b>{codigo}<b>
        """

        msg = email.message.Message()
        msg['Subject'] = "Assunto"
        msg['From'] = os.getenv('EMAIL_USERNAME')
        msg['To'] = data['email']
        password = os.getenv('APP_PASSWORD')
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        return jsonify({'message': 'Email enviado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@email_bp.route('/email/requisicao', methods=['POST'])
def email_requisicao():
    try:
        data = request.json
        corpo_email = f"""
        <p>Requisição para treinamento de modelo da clinica <b>{data['nome']}</b> de CNPJ: <b>{data['cnpj']}</b></p>
        <p>Total de imagens <b>{data['total_imagens']}</b></p>
        <p>Modelo para <b>{data['doenca']}</b><p>
        """

        msg = email.message.Message()
        msg['Subject'] = f"Requisições para treinamento de IA - Clinica {data['nome']}"
        msg['From'] = os.getenv('EMAIL_USERNAME')
        msg['To'] = os.getenv('EMAIL_USERNAME')
        password = os.getenv('APP_PASSWORD')
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        return jsonify({'message': 'Email enviado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
