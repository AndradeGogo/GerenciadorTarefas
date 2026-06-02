from Gerenciador import database
from datetime import datetime


class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100),nullable=False)
    email = database.Column(database.String(100),unique=True,nullable=False)
    senha = database.Column(database.String(255),nullable=False)
    cargo = database.Column(database.String(20),nullable=False)
    tarefas_criadas = database.relationship("Tarefa",foreign_keys="Tarefa.id_criador",backref="criador",lazy=True)
    tarefas_responsavel = database.relationship("Tarefa",foreign_keys="Tarefa.id_responsavel",backref="responsavel",lazy=True)


class Tarefa(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    titulo = database.Column(database.String(150), nullable=False)
    descricao = database.Column( database.Text, nullable=False)
    status = database.Column(database.String(50),default="Pendente")
    prioridade = database.Column(database.String(20),default="Média")
    data_criacao = database.Column(database.DateTime,default=datetime.utcnow)
    data_limite = database.Column(database.DateTime)
    data_conclusao = database.Column(database.DateTime )
    id_criador = database.Column(database.Integer,database.ForeignKey("usuario.id"),nullable=False)
    id_responsavel = database.Column(database.Integer,database.ForeignKey("usuario.id"),nullable=False)
