
from app import db,login_manager

from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.forms import  RegistrationForm, LoginForm
from app.models import User
from app.auth import bp
#from app.main import bp





@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been succesfully registered')
        return redirect(url_for('auth.login'))
    return render_template('register.html',title='Register',form=form)


@bp.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(csrf_enabled=True)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index',_external=True,_scheme='http'))
        else:
            return redirect(url_for('login',_external=True,_schema='http'))
    return render_template("login.html",title='login',form=form)

@login_manager.unauthorized_handler
def unauthorized():
    return "You are not logged in. Click here to get <a href="+ str("/login")+">back to Landing Page</a>"

@bp.route('/reset_pass', methods=['GET', 'POST'])
def reset_pass():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))