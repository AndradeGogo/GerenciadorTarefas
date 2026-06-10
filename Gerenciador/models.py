from sqlalchemy.engine import default
from Gerenciador import database, login_manager
from datetime import datetime
from flask_login import UserMixin

class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(120), nullable=False, unique=True)
    senha = database.Column(database.String(100), nullable=False)
    cargo = database.Column(database.String(20), nullable=False, default='funcionario')

    @login_manager.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))

class Tarefa(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(100), nullable=False)
    descricao = database.Column(database.String(200), nullable=False)
    status = database.Column(database.String(30),nullable=False, default='pendente')
    demanda = database.Column(database.String(20), nullable=False, default='baixa')
    data_Criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    prazo = database.Column(database.DateTime, nullable=False)
    id_Criador = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_Responsavel = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)