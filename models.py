from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from enum import Enum
db = SQLAlchemy()

class StatusRequisicao(Enum):
    REQUISITADO = 'Requisitado'
    ACEITO = 'Aceito'
    EM_EXECUCAO = 'Em_Execucao'
    CONCLUIDO = 'Concluido'
    FINALIZADO = 'Finalizado'

class Administrador(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    def __init__(self, senha, username, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.senha = senha
        self.username = username

class Pessoa(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15))
    cargo = db.Column(db.String(100))
    pacientes = db.relationship('Paciente', backref='pessoa', lazy=True)
    funcionarios = db.relationship('Funcionario', backref='pessoa', lazy=True)
    medicos = db.relationship('Medico', backref='pessoa', lazy=True)
    def __init__(self, cpf, data_nascimento, nome, telefone, cargo, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.nome = nome
        self.telefone = telefone
        self.cargo = cargo
    
class Paciente(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    id_pessoa = db.Column(db.String(36), db.ForeignKey('pessoa.id'), nullable=False)
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    tipo_sanguineo = db.Column(db.String(5), nullable=False)
    detalhes_clinicos = db.Column(db.Text)
    cep = db.Column(db.String(50))
    logradouro = db.Column(db.String(100))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    numero = db.Column(db.String(10))
    estado = db.Column(db.String(2))
    diagnosticos = db.relationship('Diagnostico', backref='paciente', lazy=True)
    def __init__(self, id_pessoa,id_clinica, sexo, tipo_sanguineo, detalhes_clinicos, cep,logradouro, bairro, cidade, numero, estado, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.id_pessoa = id_pessoa
        self.id_clinica = id_clinica
        self.sexo = sexo
        self.tipo_sanguineo = tipo_sanguineo
        self.detalhes_clinicos = detalhes_clinicos
        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.numero = numero
        self.estado = estado

medico_clinica_association = db.Table(
    'medico_clinica_association',
    db.Column('medico_id', db.String(36), db.ForeignKey('medico.id')),
    db.Column('clinica_id', db.String(36), db.ForeignKey('clinica.id'))
)

class Clinica(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True, nullable=False)
    foto_perfil = db.Column(db.Text, nullable=True)
    senha = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(50))
    logradouro = db.Column(db.String(100))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    numero = db.Column(db.String(10))
    estado = db.Column(db.String(2))
    modelo_id = db.Column(db.String(36), nullable=True)
    medicos = db.relationship('Medico', secondary=medico_clinica_association, backref='clinica')
    funcionarios = db.relationship('Funcionario', backref='clinica', lazy=True)
    pacientes = db.relationship('Paciente', backref='clinica', lazy=True)
    diagnosticos = db.relationship('Diagnostico', backref='clinica', lazy=True)
    requisicoes = db.relationship('Requisicao', backref='clinica', lazy=True)
    def __init__(self, cnpj, nome, senha, modelo_id=None ,id=None, foto_perfil=None, telefone=None,email=None,logradouro=None,bairro=None,cidade=None
                 ,numero=None,estado=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.foto_perfil = foto_perfil
        self.cnpj = cnpj
        self.nome = nome
        self.senha = senha
        self.email = email
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.numero = numero
        self.estado = estado
        self.modelo_id = modelo_id
        self.medicos = []


class Medico(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    id_pessoa = db.Column(db.String(36), db.ForeignKey('pessoa.id'), nullable=False)
    crm = db.Column(db.String(15), unique=True, nullable=False)
    especialidade = db.Column(db.String(100))
    senha = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    foto_perfil = db.Column(db.Text, nullable=True)
    verification_code = db.Column(db.String(6), nullable=True)
    verification_code_expiration = db.Column(db.DateTime, nullable=True)
    clinicas = db.relationship('Clinica', secondary=medico_clinica_association, backref='medico')
    diagnosticos = db.relationship('Diagnostico', backref='medico', lazy=True)
    def __init__(self, id_pessoa, crm, especialidade, senha, email, id=None, foto_perfil=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        if  foto_perfil is None:
            self.foto_perfil = None
        else:
            self.foto_perfil = foto_perfil
        self.id_pessoa = id_pessoa
        self.crm = crm 
        self.especialidade = especialidade
        self.senha = senha
        self.email = email
        self.clinicas = []

class Funcionario(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    id_pessoa = db.Column(db.String(36), db.ForeignKey('pessoa.id'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    especialista = db.Column(db.String(100))
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'))

    def __init__(self, id_pessoa, email, senha, especialista, id_clinica, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.id_pessoa = id_pessoa
        self.email = email
        self.senha = senha
        self.especialista = especialista
        self.id_clinica = id_clinica

class Diagnostico(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    # id_modelo = db.Column(db.String(36), db.ForeignKey('modelo.id'), nullable=False)
    modelo = db.Column(db.String(255))
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'), nullable=False)
    id_medico = db.Column(db.String(36), db.ForeignKey('medico.id'), nullable=False)
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    raio_x = db.Column(db.Text)
    id_paciente = db.Column(db.String(36), db.ForeignKey('paciente.id'), nullable=False)
    laudo_medico = db.Column(db.Text)
    mapa_calor = db.Column(db.Text)
    resultado_modelo = db.Column(db.String(255))
    resultado_real = db.Column(db.String(255))
    usada = db.Column(db.Boolean, default=False)

    def __init__(self, modelo,raio_x, id_medico, id_clinica, data_hora, id_paciente, laudo_medico, mapa_calor ,resultado_modelo, resultado_real ,id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
    
        self.modelo = modelo
        self.raio_x = raio_x
        self.id_medico = id_medico
        self.id_clinica = id_clinica
        self.data_hora = data_hora
        self.id_paciente = id_paciente
        self.laudo_medico = laudo_medico
        self.mapa_calor = mapa_calor
        self.resultado_modelo = resultado_modelo
        self.resultado_real = resultado_real
        self.usada = False

class Modelo(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(100), nullable=False)
    precisao = db.Column(db.String(15))
    acuracia = db.Column(db.String(15))
    f1score = db.Column(db.String(15))
    recall = db.Column(db.String(15))
    kappa = db.Column(db.String(15))
    filtros = db.Column(db.String(510))
    data_augmentation = db.Column(db.Boolean, default=False)
    arquivo = db.Column(db.String(255))

    def __init__(self, precisao, acuracia, f1score, recall, kappa, filtros, data_augmentation, cnpj,nome,arquivo, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.precisao = precisao
        self.acuracia = acuracia
        self.f1score = f1score
        self.recall = recall
        self.kappa = kappa
        self.filtros = filtros
        self.data_augmentation = data_augmentation
        self.arquivo = arquivo

class Requisicao(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    quantidade_imagens = db.Column(db.String(100), nullable=False)
    id_clinica = db.Column(db.String(36), db.ForeignKey('clinica.id'), nullable=False)
    data_hora = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(StatusRequisicao), default=StatusRequisicao.REQUISITADO, nullable=False)

    def __init__(self, id_clinica, data_hora, quantidade_imagens, status=StatusRequisicao.REQUISITADO, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.quantidade_imagens = quantidade_imagens
        self.id_clinica = id_clinica
        self.data_hora = data_hora
        self.status = status

   


