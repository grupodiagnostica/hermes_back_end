from flask import Blueprint, request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from models import Modelo
from models import db
from src.middleware.token import token_required
import glob
from PIL import Image
import io
import base64
import cv2
import scipy as sp
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from src.utils.camResult import cam_result

predicao_bp = Blueprint('predicao', __name__)

# Carrega o modelo .h5
diretorio_modelos = '../../models'
models = glob.glob(f'{diretorio_modelos}/model*.h5')


@predicao_bp.route('/predict/<int:model_id>', methods=['POST'])
@token_required
def predict(model_id):
    try:    

        id = request.args.get('id')
        modelo = Modelo.query.filter(Modelo.id == id).first()
        print(models)
        print(modelo.arquivo)
        if modelo:

            model_path = diretorio_modelos + modelo.arquivo
            model = tf.keras.models.load_model(model_path)

            image_orig = request.files['image'].read()
            image_orig = cv2.imdecode(np.frombuffer(image_orig, np.int8), cv2.IMREAD_COLOR)
            
            image = cv2.equalizeHist(cv2.resize(cv2.cvtColor(image_orig, cv2.COLOR_RGB2GRAY), (224, 224)))
            image = np.array(image) / 255
            image = image.reshape(-1, 224, 224, 1) 

            image_orig = cv2.resize(image_orig, (224, 224))
            
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

            image_pil = Image.fromarray(map_act).convert('RGB')

            img_byte_array = io.BytesIO()
            image_pil.save(img_byte_array, format='JPEG')

            imagem_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
            data = {'predictions': result, 'image':imagem_base64}    

            response = jsonify(data)

            response.headers['Access-Control-Allow-Origin'] = '*'

            del model
            return response
        else:
            return jsonify({'message': 'Modelo não encontrado'}), 404
    except Exception as e:
        print(e)
        response = jsonify({'error': str(e)})
        return response
