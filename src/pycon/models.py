# -*- coding: utf-8 -*-
import os
import string
from base64 import b64encode

from pycon.riddles import app, db


class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __init__(self, active):
        self.active = active

    @classmethod
    def ensure(cls):
        """ Make sure settings exist."""
        settings = cls.query.first()
        if not settings:
            settings = Settings(active=False)
            db.session.add(settings)
            db.session.commit()
        return settings

    @classmethod
    def is_active(cls):
        """Check if application should be active."""
        settings = cls.ensure()
        return settings.active

class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    value = db.Column(db.String(12), unique=True, nullable=False)

    def __init__(self, value):
        self.value = value

    @classmethod
    def generate(cls):
        while True:
            bytes = os.urandom(9)
            encoded = b64encode(bytes)
            for letter in encoded:
                if letter not in string.letters and letter not in string.digits:
                    break
            else:
                break
        return cls(encoded)

    def is_used(self):
        return bool(self.user.count())

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    token_id = db.Column(db.Integer, db.ForeignKey('token.id'), nullable=False)
    token = db.relationship(Token, primaryjoin=token_id == Token.id,
        backref=db.backref('user', lazy='dynamic'))

    def __init__(self, email, token_id):
        self.email = email
        self.token_id = token_id

    def __repr__(self):
        return u'<User %r>' % self.email

    def get_progress(self):
        return self.progress.order_by(Progress.ts.desc()).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

    def get_stage(self):
        progress = self.get_progress()
        return progress.stage

    def add_stage(self, stage):
        progress = Progress(stage=stage, user_id=self.id)
        db.session.add(progress)
        db.session.commit()
        return progress

    def get_num_of_tries(self):
        return self.tries.count()

    def add_try(self, answer):
        try_ = Try(user_id=self.id, stage=self.get_stage(), answer=answer)
        db.session.add(try_)
        db.session.commit()
        return try_


class Progress(db.Model):
    __tablename__ = 'progress'
    __table_args__ = (
        db.UniqueConstraint('stage', 'user_id', name='user_stage_unique'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    stage = db.Column(db.String(64), nullable=False)
    ts = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, primaryjoin=user_id == User.id,
        backref=db.backref('progress', lazy='dynamic'))

    def __init__(self, stage, user_id):
        self.stage = stage
        self.user_id = user_id

class Try(db.Model):
    __tablename__ = 'tries'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ts = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, primaryjoin=user_id == User.id,
        backref=db.backref('tries', lazy='dynamic'))
    stage = db.Column(db.String(64), nullable=False)
    answer = db.Column(db.String(app.config['MAX_ANSWER_LENGTH']), nullable=True)

    def __init__(self, user_id, stage, answer):
        self.user_id = user_id
        self.stage = stage
        self.answer = answer
