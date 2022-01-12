from app import db,login_manager
from app.utils.chromedriverinit import BrowserDriverInit
from app.utils.data_extractor import crawl_followers,audit_followers
from flask import request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.main.forms import SearchForm
from app.models import User
from app.main import bp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/profile/<int:profile_id>')
def profile(profile_id):
    return render_template('profile.html')


@bp.route('/home',methods=['GET','POST'])
@bp.route('/',methods=['GET','POST'])
#@login_required
def index():
    searchform = SearchForm()
    if searchform.validate_on_submit():
        with BrowserDriverInit() as browser:
            ig_username = searchform.ig_username.data
            followers = crawl_followers(browser,ig_username)
            fake_followers = audit_followers(browser, followers)
            #fake_followers = defaultdict(None, {'nu11byt3sss': {'score': 1.5}, 'pascaleochoa3': {'score': 1.5}, 'auroraflores242': {'score': 1.5}, 'sariyahsosa': {'score': 1.5}})
            followers = 100
            return render_template('index.html',form=searchform,ig_username=ig_username,follower_count=followers,fake_count=len(fake_followers))

    return render_template('index.html', form=searchform,follower_count='100',fake_count='10')


@bp.route('/test',methods=['GET'])
def test():
    return render_template('test.html')