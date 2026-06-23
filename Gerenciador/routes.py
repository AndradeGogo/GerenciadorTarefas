from flask import render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from Gerenciador import app, database, bcrypt
from Gerenciador.forms import FormLogin, FormCriarConta, FormTarefa
from Gerenciador.models import Usuario, Tarefa


@app.route('/', methods=['GET', 'POST'])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario, remember=True)
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
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('criarconta.html', form=formcriarconta)


@app.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    id_usuario_int = int(id_usuario)
    usuario = Usuario.query.get(id_usuario_int)

    if id_usuario_int == int(current_user.id):
        if current_user.cargo == 'gerente':
            form = FormTarefa()
            usuarios_sistema = Usuario.query.all()
            form.id_responsavel.choices = [(u.id, u.nome) for u in usuarios_sistema]

            if form.validate_on_submit():
                nova_tarefa = Tarefa(
                    titulo=form.titulo.data,
                    descricao=form.descricao.data,
                    demanda=form.demanda.data,
                    prazo=form.prazo.data,
                    id_Criador=current_user.id,
                    id_Responsavel=form.id_responsavel.data
                )
                database.session.add(nova_tarefa)
                database.session.commit()
                flash('Tarefa atribuída com sucesso!', 'success')
                return redirect(url_for('perfil', id_usuario=current_user.id))
        else:
            form = None  # Se for funcionário, não gera o formulário no backend

        tarefas = Tarefa.query.filter_by(id_Responsavel=current_user.id).all()
        return render_template('perfil.html', usuario=current_user, form=form, tarefas=tarefas)

    else:
        tarefas_outro = Tarefa.query.filter_by(id_Responsavel=id_usuario_int).all()
        return render_template('perfil.html', usuario=usuario, form=None, tarefas=tarefas_outro)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

