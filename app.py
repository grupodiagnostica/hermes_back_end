from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2
from flask_cors import CORS
app = Flask(__name__)


CORS(app)
# Carregue o modelo .h5
model = tf.keras.models.load_model('./modeloXception.h5')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print(request.files)
        # print(model)
        # Receba a imagem do front-end
        image = request.files['image'].read()


        # Pré-processamento da imagem, dependendo do seu modelo
        # Exemplo de redimensionamento de imagem para o tamanho esperado
        image = tf.image.decode_image(image, channels=3)
        image = tf.image.resize(image, (224, 224))
        image = tf.expand_dims(image, axis=0)  # Adicione uma dimensão de lote

        # Converter a imagem para preto e branco
        # image = tf.image.rgb_to_grayscale(image)

        # Normalizar os valores dos pixels para estar na faixa entre 0 e 1
        image = tf.cast(image, tf.float32) / 255.0
        print(image)

        # Faça a previsão
        predictions = model.predict(image)
        print("opaaaaaaaaaaaaa")
        # Converta as previsões em uma lista Python
        predictions = predictions.tolist()
        print(predictions)
        data = {'predictions': predictions}
        response = jsonify(data)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        response = jsonify({'error': str(e)})
        return response

if __name__ == '__main__':
    app.run(debug=True)
