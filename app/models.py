from app import db
import datetime
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import rq
import redis
from flask import current_app, url_for

rel = db.Table('rel',
    db.Column('handle_id',db.Integer,db.ForeignKey('handle.handle_id')),
    db.Column('follower_id',db.Integer,db.ForeignKey('fakefollower.follower_id'))
               )
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String(20),index=True,unique=True)
    like_count = db.Column(db.Integer,unique=True)
    comment_count = db.Column(db.Integer,unique=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('handle.handle_id'))

class Handle(db.Model):
    __tablename__ = "handle"
    handle_id = db.Column(db.Integer, primary_key=True)
    ig_handle = db.Column(db.String(100),index=True,unique=True)
    ig_follower_count = db.Column(db.Integer)
    ig_followed_count = db.Column(db.Integer)

    ig_fake_follower = db.relationship("FakeFollower",secondary=rel,backref=db.backref('ig_handle', lazy='dynamic' ))

    def __repr__(self):
        return f'{self.ig_handle - self.ig_follower_count - self.ig_fake_followers}'

class FakeFollower(db.Model):
    __tablename__ = "fakefollower"
    follower_id = db.Column(db.Integer, primary_key=True)
    follower_handle = db.Column(db.String(100),index=True)
    follower_score = db.Column(db.Integer)
    def __repr__(self):
        return f'{self.fake_username - self.score - self.followed_acct}'

class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100
