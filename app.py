from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from flask_cors import CORS

from flask import Flask, redirect, render_template
import uuid
from models import db, Medico
from routes.medico import medico_bp
from routes.pessoa import pessoa_bp
from routes.paciente import paciente_bp
from routes.clinica import clinica_bp
from routes.doenca import doenca_bp
from routes.diagnostico import diagnostico_bp
from routes.funcionario import funcionario_bp
from routes.modelo import modelo_bp
from models import Pessoa
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import base64
import scipy as sp
from scipy import ndimage
from PIL import Image
import io
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
from oauthlib.oauth2 import WebApplicationClient
import random
import bcrypt
from datetime import datetime, timedelta
import yagmail
from sendEmail import send
from sendEmail import send_mail
load_dotenv()

app = Flask(__name__)

CORS(app, origins='*')
CORS(pessoa_bp, origins='*')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

# ---------------------------- email ------------------- refatorar depois

mail = Mail(app)

def enviar_email_codigo_verificacao(destinatario, verification_code):
    try:
        sender_email = "grupodiagnosticatic@gmail.com"
        receiver_email = destinatario
        subject = "Codigo de verificação"
        body = f'Seu código de verificação é: {verification_code}'

        yag = yagmail.SMTP(sender_email, oauth2_file='./client.json')
        yag.send(to=receiver_email, subject=subject, contents=body)
        yag.close()

        return True
    except Exception as e:
        print(str(e))
        return False
    
def generate_verification_code():
    # Gera um código de verificação de 6 dígitos
    return str(random.randint(100000, 999999))

@app.route('/enviar-codigo-verificacao', methods=['POST'])
def enviar_codigo_verificacao():
    try:
        data = request.json
        email = data['email']

        medico = Medico.query.filter_by(email=email).first()

        if medico:
            # Gerar um código de verificação
            verification_code = generate_verification_code()

            # Definir o código e o tempo de expiração no modelo
            medico.verification_code = verification_code
            medico.verification_code_expiration = datetime.utcnow() + timedelta(minutes=10)  # Pode ajustar o tempo de expiração conforme necessário

            db.session.commit()

            # Enviar e-mail com o código de verificação
            send('email.teste.dvs@gmail.com', 'grupodiagnosticatic@gmail.com' , "Codigo de verificação", verification_code)
            return jsonify({'message': 'Um código de verificação foi enviado para o seu e-mail'})
        else:
            return jsonify({'error': 'Médico não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/redefinir-senha', methods=['POST'])
def redefinir_senha():
    try:
        data = request.json
        email = data['email']
        verification_code = data['verification_code']
        nova_senha = data['nova_senha']

        medico = Medico.query.filter_by(email=email).first()

        if medico and medico.verification_code == verification_code and medico.verification_code_expiration > datetime.utcnow():
            # Atualizar a senha e limpar o código de verificação
            medico.senha = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            medico.verification_code = None
            medico.verification_code_expiration = None

            db.session.commit()

            return jsonify({'message': 'Senha redefinida com sucesso'})
        else:
            return jsonify({'error': 'Código inválido ou expirado'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

# ------------------------------------ email -----------------------


# Carrega o modelo .h5
model1 = './modeloXception.h5'
model2 = './model-24-0.9730-2023-11-19.h5'
models = []
models.append(model1)
models.append(model2)



def cam_result(features, results, gap_weights) -> tuple:
  # there is only one image in the batch so we index at `0`
  features_for_img = features[0]
  prediction = results[0][0]
  # there is only one unit in the output so we get the weights connected to it
  class_activation_weights = gap_weights[:,0]
  # upsample to the image size
  class_activation_features = sp.ndimage.zoom(features_for_img, (224/7, 224/7, 1), order=2)
  #spline interpolation of order = 2 (G search)
  # compute the intensity of each feature in the CAM
  cam_output  = np.dot(class_activation_features, class_activation_weights)
  return prediction, cam_output

db_user = 'hermesuser'
db_password = '123'
db_host = '164.152.36.125'
db_port = '5432'
db_name = 'hermesdb'

connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db.init_app(app)

app.register_blueprint(pessoa_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(modelo_bp)
app.register_blueprint(funcionario_bp)
app.register_blueprint(doenca_bp)
app.register_blueprint(diagnostico_bp)
app.register_blueprint(clinica_bp)
app.register_blueprint(medico_bp)


@app.route('/predict/<int:model_id>', methods=['POST'])
def predict(model_id):
    try:
        print(model_id)
        model_path = models[model_id - 1]

        model = tf.keras.models.load_model(model_path)

        image = request.files['image'].read()


        image = tf.image.decode_image(image, channels=3)
        image = tf.image.resize(image, (224, 224))
        image = tf.expand_dims(image, axis=0) 

     
        
        if model_id == 2:
            gap_weights = model.layers[-1].get_weights()[0]
            cam_model  = tf.keras.models.Model(inputs=[model.input], outputs=[model.layers[-8].output, model.output])
            image = tf.image.rgb_to_grayscale(image)
            image = tf.cast(image, tf.float32) / 255.0
            features, results = cam_model.predict(image)
            result, map_act = cam_result(features, results, gap_weights)
            # Converter ndarray para uma imagem PIL no modo 'RGB'
            if map_act.ndim == 2:
                map_act = np.stack((map_act,) * 3, axis=-1)
            
            # Normalização e ajuste do intervalo
            map_act = (map_act - np.min(map_act)) / (np.max(map_act) - np.min(map_act))
            map_act = (map_act * 255.0).astype('uint8')
            # map_act = np.stack([map_act, map_act, map_act], axis=-1)
            image_pil = Image.fromarray(map_act)

            # Salvar a imagem PIL em um buffer de bytes
            img_byte_array = io.BytesIO()
            image_pil.save(img_byte_array, format='JPEG')

            # Converter o buffer de bytes para base64
            imagem_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
            data = {'predictions': result.tolist(), 'image':imagem_base64}
            print(data.get('predictions'))
            
        else:
            image = tf.cast(image, tf.float32) / 255.0
            predictions = model.predict(image)
            predictions = predictions.tolist()
            data = {'predictions': predictions}


        response = jsonify(data)

        print('foi aqui')
        if model_id == 3:
            response.headers['Content-Disposition'] = 'attachment; filename=image.bin'
            response.headers['Content-Type'] = 'image/octet-stream'
        response.headers['Access-Control-Allow-Origin'] = '*'

        del model
        return response
    except Exception as e:
        response = jsonify({'error': str(e)})
        return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
