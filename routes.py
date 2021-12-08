from app import app,db
from utils.chromedriverinit import BrowserDriverInit
from utils.data_extractor import crawl_followers,audit_followers
from flask import request, render_template, flash, redirect, url_for
from werkzeug.urls import url_parse
from forms import SearchForm
from collections import defaultdict



@app.route('/',methods=['GET','POST'])
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