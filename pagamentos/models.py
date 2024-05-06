from pagamentos import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuarios.query.get(int(id_usuario))

class Usuarios(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

class Webhook(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False)
    valor = database.Column(database.Integer, nullable=False)
    forma_pagamento = database.Column(database.String, nullable=False)
    parcelas = database.Column(database.Integer, nullable=False)
    resposta = database.Column(database.String, nullable=False)
    data_evento = database.Column(database.DateTime, nullable=False, default=datetime.utcnow().date())
