from flask import Flask
from flask_cors import CORS
from flask import Flask, redirect, render_template
from models import db, Diagnostico
from src.routes.medico import medico_bp
from src.routes.pessoa import pessoa_bp
from src.routes.paciente import paciente_bp
from src.routes.clinica import clinica_bp
from src.routes.diagnostico import diagnostico_bp
from src.routes.funcionario import funcionario_bp
from src.routes.login import login_bp
from src.routes.email import email_bp
from src.routes.modelo import modelo_bp
from src.routes.requisicao import requisicao_bp
from src.routes.predicao import predicao_bp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from dotenv import load_dotenv
import os


load_dotenv("env")

app = Flask(__name__)

CORS(app, origins='*')
CORS(pessoa_bp, origins='*')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

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
app.register_blueprint(predicao_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
