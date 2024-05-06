import json

from flask import render_template, redirect, url_for, request, flash, abort, jsonify
from pagamentos import app, database, bcrypt
from pagamentos.forms import FormEntrar, FormCadastrar
from pagamentos.models import Usuarios, Webhook
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def home():
    return redirect(url_for('signin_login'))


@app.route("/signin_login", methods=['GET', 'POST'])
def signin_login():
    form_entrar = FormEntrar()
    form_cadastrar = FormCadastrar()

    if form_entrar.validate_on_submit() and 'botao_entrar' in request.form:
        usuario = Usuarios.query.filter_by(email=form_entrar.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_entrar.senha.data):
            flash(f'Login efetuado com sucesso no e-mail {form_entrar.email.data}', 'alert-success')
            login_user(usuario, remember=form_entrar.lembrar_dados.data)
            return redirect(url_for('eventos'))
        else:
            flash(f'Falha ao tentar entrar no e-mail: {form_entrar.email.data}', 'alert-danger')
    if form_cadastrar.validate_on_submit() and 'botao_cadastrar' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_cadastrar.senha.data)
        usuario = Usuarios(username=form_cadastrar.username.data, email=form_cadastrar.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Cadastro efetuado com sucesso no e-mail {form_cadastrar.email.data}', 'alert-success')
        return redirect(url_for('eventos'))

    return render_template('signin_login.html', form_entrar=form_entrar, form_cadastrar=form_cadastrar)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Você saiu.', 'alert-success')
    return redirect(url_for('signin_login'))

@app.route('/eventos')
@login_required
def eventos():
    lista_eventos = Webhook.query.all()
    return render_template('eventos.html', lista_eventos=lista_eventos)

@app.route('/webhook', methods=['POST'])
def webhook():
    response = {"status": 200}
    conteudo = request.data.decode('utf-8')
    conteudo_json = json.loads(conteudo)

    resposta = ""

    if conteudo_json['status'] == "aprovado":
        resposta = f'Liberar acesso do e-mail: {conteudo_json["email"]}, Enviar mensagem de boas vindas para o email: {conteudo_json["email"]}'

    elif conteudo_json['status'] == "recusado":
        resposta = "Seu pagamento foi recusado"
    elif conteudo_json['status'] == "reembolsado":
        resposta = f'Remover acesso do e-mail: {conteudo_json["email"]}'

    print(resposta)

    evento = Webhook(nome=conteudo_json['nome'], email=conteudo_json['email'], status=conteudo_json['status'],
                     valor=conteudo_json['valor'], forma_pagamento=conteudo_json['forma_pagamento'],
                     parcelas=conteudo_json['parcelas'], resposta=resposta)
    database.session.add(evento)
    database.session.commit()

    return response

