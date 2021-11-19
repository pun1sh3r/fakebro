from app import app,db
from utils.chromedriverinit import BrowserDriverInit
from utils.data_extractor import crawl_followers,audit_followers
from flask import request, render_template, flash, redirect, url_for
from werkzeug.urls import url_parse
from forms import SearchForm




@app.route('/',methods=['GET','POST'])
def index():
    searchform = SearchForm()
    if searchform.validate_on_submit():
        with BrowserDriverInit() as browser:
            ig_username = searchform.ig_username.data
            followers = crawl_followers(browser,ig_username)
            fake_followers = audit_followers(browser, followers)
            #fake_followers = 17
            #followers = 100
            return render_template('index.html',form=searchform,ig_username=ig_username,follower_count=len(followers),fake_count=len(fake_followers))

    return render_template('index.html', form=searchform,follower_count='',fake_count='')