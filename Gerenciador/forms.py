from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from Gerenciador.models import Usuario


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Fazer Login')


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])

    cargo = SelectField('Seu Cargo / Função', choices=[
        ('gerente', 'Gerente'),
        ('funcionario', 'Funcionário')
    ], validators=[DataRequired()])

    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmeSenha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado. Faça login para continuar")


class FormTarefa(FlaskForm):
    titulo = StringField('Título da Tarefa', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    demanda = SelectField('Prioridade/Demanda', choices=[('baixa', 'Baixa'), ('media', 'Média'), ('alta', 'Alta')], default='media')
    prazo = DateField('Prazo de Conclusão', validators=[DataRequired()])
    id_responsavel = SelectField('Responsável pela Tarefa', coerce=int, validators=[DataRequired()])
    botao_confirmacao = SubmitField('Criar Tarefa')