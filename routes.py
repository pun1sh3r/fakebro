from app import app,db,login_manager
from utils.chromedriverinit import BrowserDriverInit
from utils.data_extractor import crawl_followers,audit_followers
from flask import request, render_template, flash, redirect, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from forms import SearchForm, RegistrationForm, LoginForm
from collections import defaultdict
from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/',methods=['GET','POST'])
@login_required
def index():
    searchform = SearchForm()
    if searchform.validate_on_submit():
        with BrowserDriverInit() as browser:
            ig_username = searchform.ig_username.data
            #followers = crawl_followers(browser,ig_username)
            #fake_followers = audit_followers(browser, followers)
            fake_followers = defaultdict(None, {'nu11byt3sss': {'score': 1.5}, 'pascaleochoa3': {'score': 1.5}, 'auroraflores242': {'score': 1.5}, 'sariyahsosa': {'score': 1.5}})
            followers = 100
            return render_template('index.html',form=searchform,ig_username=ig_username,follower_count=followers,fake_count=len(fake_followers))

    return render_template('index.html', form=searchform,follower_count='100',fake_count='10')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html',title='Register',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(csrf_enabled=True)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index',_external=True,_scheme='http'))
        else:
            return redirect(url_for('login',_external=True,_schema='http'))
    return render_template("login.html",title='login',form=form)

@login_manager.unauthorized_handler
def unauthorized():
    return "You are not logged in. Click here to get <a href="+ str("/login")+">back to Landing Page</a>"




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

