from flask import render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from Gerenciador import app, database, bcrypt
from Gerenciador.forms import FormLogin, FormCriarConta
from Gerenciador.models import Usuario


@app.route('/', methods=['GET', 'POST'])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario, remember=True)
            # Redireciona passando o ID do usuário
            return redirect(url_for('perfil', id_usuario=usuario.id))
        else:
            flash('E-mail ou senha incorretos.', 'danger')
    return render_template('homepage.html', form=formLogin)


@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha_criptografada = bcrypt.generate_password_hash(formcriarconta.senha.data).decode('utf-8')

        usuario = Usuario(
            nome=formcriarconta.username.data,
            email=formcriarconta.email.data,
            senha=senha_criptografada,
            cargo=formcriarconta.cargo.data
        )

        database.session.add(usuario)
        database.session.commit()

        login_user(usuario, remember=True)
        # Redireciona passando o ID do usuário recém-criado
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('criarconta.html', form=formcriarconta)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


# Rota atualizada para receber o ID do usuário como um número inteiro
@app.route('/perfil/<int:id_usuario>')
@login_required
def perfil(id_usuario):
    # Busca o usuário no banco de dados pelo ID ou retorna erro 404 se não existir
    usuario_visitado = Usuario.query.get_or_404(id_usuario)

    # Verifica se o usuário logado é o dono do perfil visitado
    e_o_dono = current_user.id == usuario_visitado.id

    # Passa o objeto completo do usuário e o booleano de verificação para o HTML
    return render_template('perfil.html', usuario=usuario_visitado, e_o_dono=e_o_dono)