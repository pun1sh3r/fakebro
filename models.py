from app import app, db

class UserName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ig_username = db.Column(db.String(100),index=True,unique=True)
    ig_follower_count = db.Column(db.Integer)
    ig_fake_followers = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.ig_username - self.ig_follower_count - self.ig_fake_followers}'

class FakeFollower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fake_username = db.Column(db.String(100),index=True,unique=True)
    score = db.Column(db.Integer)
    followed_acct = db.Column(db.Integer, db.ForeignKey(UserName.id),nullable=False)

    def __repr__(self):
        return f'{self.fake_username - self.score - self.followed_acct}'

