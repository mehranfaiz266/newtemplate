from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from . import db, login_manager, get_fernet
from .models import User, APICredential
from .forms import LoginForm, RegisterForm, CredentialForm
from flask import current_app as app


@app.route('/')
@login_required
def index():
    creds = APICredential.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', creds=creds)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('User already exists')
        else:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/credentials/add', methods=['GET', 'POST'])
@login_required
def add_credential():
    form = CredentialForm()
    if form.validate_on_submit():
        f = get_fernet(app)
        encrypted = f.encrypt(form.api_secret.data.encode())
        cred = APICredential(
            user_id=current_user.id,
            name=form.name.data,
            api_key=form.api_key.data,
            api_secret_encrypted=encrypted
        )
        db.session.add(cred)
        db.session.commit()
        flash('Credential saved')
        return redirect(url_for('index'))
    return render_template('add_credential.html', form=form)


@app.route('/credentials/<int:cred_id>/view')
@login_required
def view_credential(cred_id):
    cred = APICredential.query.get_or_404(cred_id)
    if cred.user_id != current_user.id:
        flash('Not authorized')
        return redirect(url_for('index'))
    f = get_fernet(app)
    secret = f.decrypt(cred.api_secret_encrypted).decode()
    return render_template('view_credential.html', cred=cred, secret=secret)
