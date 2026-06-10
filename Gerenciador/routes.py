from Gerenciador import app
from flask import render_template, url_for
from flask_login import login_required
from Gerenciador.forms import FormLogin, FormCriarConta

@app.route('/', methods=['GET','POST'])
def homepage():
    formLogin = FormLogin()
    return render_template('homepage.html', form=formLogin )

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    return render_template('criarconta.html', form=formcriarconta)

@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)
