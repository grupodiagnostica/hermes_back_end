from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from flask_cors import CORS

from flask import Flask, redirect, render_template
from models import db, Diagnostico
from routes.medico import medico_bp
from routes.pessoa import pessoa_bp
from routes.paciente import paciente_bp
from routes.clinica import clinica_bp
from routes.diagnostico import diagnostico_bp
from routes.funcionario import funcionario_bp
from routes.login import login_bp
from routes.email import email_bp
from routes.modelo import modelo_bp
from routes.requisicao import requisicao_bp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import base64
import scipy as sp
from scipy import ndimage
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import io
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
from oauthlib.oauth2 import WebApplicationClient
from datetime import datetime, timedelta
import glob

load_dotenv("env")

app = Flask(__name__)

CORS(app, origins='*')
CORS(pessoa_bp, origins='*')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

# Carrega o modelo .h5
diretorio_modelos = './models'
models = glob.glob(f'{diretorio_modelos}/model*.h5')


def cam_result(features, results, gap_weights) -> tuple:
  classes = ['PNEUMONIA', 'COVID19', 'TUBERCULOSE', 'NORMAL']
  def softmax(x: list):
    """Calcula os valores softmax para cada conjunto de pontuações em x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

  # there is only one image in the batch so we index at `0`
  features_for_img = features[0]
  print(softmax(results[0]))
  prediction = [classes[np.argmax(results[0])], str(np.max(softmax(results[0])))]
  # there is only one unit in the output so we get the weights connected to it
  class_activation_weights = gap_weights[:,0]
  # upsample to the image size
  class_activation_features = sp.ndimage.zoom(features_for_img, (224/14, 224/14, 1), order=2)
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
app.register_blueprint(funcionario_bp)
app.register_blueprint(diagnostico_bp)
app.register_blueprint(clinica_bp)
app.register_blueprint(medico_bp)
app.register_blueprint(login_bp)
app.register_blueprint(email_bp)
app.register_blueprint(modelo_bp)
app.register_blueprint(requisicao_bp)


# Obtendo a data e hora atuais
data_atual = datetime.now()

# Formatando a data
formato_data = "%Y-%m-%d"
data_formatada = data_atual.strftime(formato_data)


@app.route('/retroalimentacao/<int:model_id>', methods=['POST'])
def retroalimentacao(model_id):
    try:
        print(model_id)
        model_path = models[model_id - 1]
        id_medico = request.args.get('id_medico')
        model = tf.keras.models.load_model(model_path)
        query = Diagnostico.query
        # Execute a consulta
        diagnosticos = query.all()
        if id_medico:
            query = query.filter(Diagnostico.id_medico == id_medico)

        # Converta os resultados em um formato JSON
        images_orig = []
        images = []
        labels = []
        for diagnostico in diagnosticos:
            images_orig.append(diagnostico.raio_x)
            labels.append(diagnostico.resultado_real)
        for image_orig in images_orig:
            image = cv2.imdecode(np.frombuffer(image_orig, np.int8), cv2.IMREAD_COLOR)
            
            image = cv2.equalizeHist(cv2.resize(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), (224, 224)))
            image = np.array(image) / 255
            image = image.reshape(-1, 224, 224, 1) 

            image_orig = cv2.resize(image, (224, 224))
            images.append(image_orig)
        
        model.fit(images, labels, epochs=5, batch_size=32)
        tf.keras.models.save_model(model,f'./model_{data_formatada}')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response = jsonify({"data": "Retroalimentação concluida"})
        del model
        return response
    except Exception as e:
        response = jsonify({'error': str(e)})
        return response

@app.route('/predict/<int:model_id>', methods=['POST'])
def predict(model_id):
    try:    
        model_path = models[model_id]
        model = tf.keras.models.load_model(model_path)

        image_orig = request.files['image'].read()
        image_orig = cv2.imdecode(np.frombuffer(image_orig, np.int8), cv2.IMREAD_COLOR)
        
        image = cv2.equalizeHist(cv2.resize(cv2.cvtColor(image_orig, cv2.COLOR_RGB2GRAY), (224, 224)))
        image = np.array(image) / 255
        image = image.reshape(-1, 224, 224, 1) 

        image_orig = cv2.resize(image_orig, (224, 224))
        
        if model_id == 1:

            gap_weights = model.layers[-1].get_weights()[0]
            cam_model  = tf.keras.models.Model(inputs=[model.input], outputs=[model.layers[-8].output, model.output])
            features, results = cam_model.predict(image)
            print(results)
            result, map_act = cam_result(features, results, gap_weights)

            map_act = cv2.normalize(map_act, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 10))
            ax1.set_title('Imagem original')
            ax1.imshow(image_orig)
            ax1.set_xticks([])
            ax1.set_yticks([])

            ax2.set_title('Imagem de calor')
            color = ax2.imshow(map_act, cmap='jet')
            ax2.imshow(image_orig, alpha=.6)
            ax2.set_xticks([])
            ax2.set_yticks([])

            fig.colorbar(color, ax=ax2, shrink=.7, location='left', label='Ativação do modelo')
            plt.tight_layout()
            fig.canvas.draw()
            map_act = np.array(fig.canvas.renderer.buffer_rgba())

            # map_act = np.stack([map_act, map_act, map_act], axis=-1)
            image_pil = Image.fromarray(map_act).convert('RGB')

            # Salvar a imagem PIL em um buffer de bytes
            img_byte_array = io.BytesIO()
            image_pil.save(img_byte_array, format='JPEG')

            # Converter o buffer de bytes para base64
            imagem_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
            data = {'predictions': result, 'image':imagem_base64}    
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
        print(e)
        response = jsonify({'error': str(e)})
        return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
