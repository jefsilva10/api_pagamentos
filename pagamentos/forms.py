from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pagamentos.models import Usuarios

#Token = 'uhdfaAADF123'
class FormEntrar(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar-me')
    botao_entrar = SubmitField('Entrar')


class FormCadastrar(FlaskForm):
    username = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    token = StringField('Token', validators=[DataRequired()])
    botao_cadastrar = SubmitField('Cadastrar')

    def validate_email(self, email):
        usuario = Usuarios.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado.')

    def validate_token(self, token):
        if token.data != "uhdfaAADF123":
            raise ValidationError('Token incorreto, tente novamente.')





