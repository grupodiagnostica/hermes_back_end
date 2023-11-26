from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from flask_cors import CORS

from flask import Flask
import uuid
from models import db
from routes.pessoa import pessoa_bp
from routes.paciente import paciente_bp
from routes.clinica import clinica_bp
from routes.doenca import doenca_bp
from routes.diagnostico import diagnostico_bp
from routes.funcionario import funcionario_bp
from routes.medico import medico_bp
from routes.modelo import modelo_bp
from models import Pessoa
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import base64
import scipy as sp
from scipy import ndimage
from PIL import Image
import io



app = Flask(__name__)

CORS(app, origins='*')
CORS(pessoa_bp, origins='*')
app.config['JWT_SECRET_KEY'] = 'hermes123'
jwt = JWTManager(app)

# custom_optimizer = tf.optimizers.Adam(learning_rate=0.001, name='CustomAdam')

# # Custom Adam optimizer with weight decay
# class AdamW(tf.keras.optimizers.Adam):
#     def __init__(self, weight_decay, use_ema=False,ema_momentum=None,jit_compile=None, ema_overwrite_frequency=None, *args, **kwargs):
#         super(AdamW, self).__init__(*args, **kwargs)
#         self.weight_decay = weight_decay
#         self.use_ema = use_ema
#         self.ema_momentum = ema_momentum
#         self.jit_compile = jit_compile
#         self.ema_overwrite_frequency = ema_overwrite_frequency
#         self._set_hyper('weight_decay', weight_decay)

#     def _resource_apply_dense(self, grad, var, apply_state=None):
#         var_device, var_dtype = var.device, var.dtype.base_dtype
#         lr_t = self.lr
#         if apply_state is not None and 'lr_t' in apply_state:
#             lr_t = apply_state['lr_t']
#         lr_t = lr_t * (1.0 - self.weight_decay)
#         var_update = super(AdamW, self)._resource_apply_dense(grad, var, apply_state)
#         return var_update.assign(var_update.read() - lr_t * var)
    
#     def get_config(self):
#         config = super(AdamW, self).get_config()
#         config.update({'weight_decay': self.weight_decay, 'ema_momentum': self.ema_momentum})
#         return config


# Example of loading the model
# custom_optimizer = AdamW(weight_decay=1e-5, ema_momentum=0.9, use_ema=True, ema_overwrite_frequency=10, jit_compile=z)
# custom_optimizer = tf.keras.optimizers.AdamW(
#     learning_rate=0.001,
#     weight_decay=0.004,
#     beta_1=0.9,
#     beta_2=0.999,
#     epsilon=1e-07,
#     amsgrad=False,
#     clipnorm=None,
#     clipvalue=None,
#     global_clipnorm=None,
#     use_ema=False,
#     ema_momentum=0.99,
#     ema_overwrite_frequency=None,
#     jit_compile=True,
#     name='AdamW'
# )



# Carrega o modelo .h5
model1 = tf.keras.models.load_model('./modeloXception.h5')
# model2 = tf.keras.models.load_model('./CNN_modelvgg19.h5')
# model2 = tf.keras.models.load_model('./model-13-0.9788-27092023.h5', custom_objects={'Custom>Adam': custom_optimizer}, compile=True, options=None)
models = []
models.append(model1)
# models.append(model2)


# gap_weights = model2.layers[-1].get_weights()[0]
# cam_model  = tf.keras.models.Model(inputs=[model2.input], outputs=[model2.layers[-8].output, model2.output])

# def cam_result(features, results) -> tuple:
#   # there is only one image in the batch so we index at `0`
#   features_for_img = features[0]
#   prediction = results[0][0]
#   # there is only one unit in the output so we get the weights connected to it
#   class_activation_weights = gap_weights[:,0]
#   # upsample to the image size
#   class_activation_features = sp.ndimage.zoom(features_for_img, (224/7, 224/7, 1), order=2)
#   #spline interpolation of order = 2 (G search)
#   # compute the intensity of each feature in the CAM
#   cam_output  = np.dot(class_activation_features, class_activation_weights)
#   return prediction, cam_output

db_user = 'hermesuser'
db_password = '123'
db_host = '129.148.52.111'
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

        image = request.files['image'].read()


        image = tf.image.decode_image(image, channels=3)
        image = tf.image.resize(image, (224, 224))
        image = tf.expand_dims(image, axis=0) 

     
        
        # if model_id == 2:
        #     image = tf.image.rgb_to_grayscale(image)
        #     image = tf.cast(image, tf.float32) / 255.0
        #     features, results = cam_model.predict(image)
        #     result, map_act = cam_result(features, results)
        # # Converter ndarray para uma imagem PIL no modo 'RGB'
        #     image_pil = Image.fromarray(map_act.astype('uint8')).convert('RGB')

        #     # Salvar a imagem PIL em um buffer de bytes
        #     img_byte_array = io.BytesIO()
        #     image_pil.save(img_byte_array, format='JPEG')

        #     # Converter o buffer de bytes para base64
        #     imagem_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
        #     data = {'predictions': result.tolist(), 'image':imagem_base64}
        #     print(data.get('predictions'))
            
        # else:
        #     model = models[model_id - 1]
        #     image = tf.cast(image, tf.float32) / 255.0
        #     predictions = model.predict(image)
        #     predictions = predictions.tolist()
        #     data = {'predictions': predictions}

        model = models[model_id - 1]
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
        return response
    except Exception as e:
        response = jsonify({'error': str(e)})
        return response

if __name__ == '__main__':
    app.run(debug=True,host="localhost", port=5000)
