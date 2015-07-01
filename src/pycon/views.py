# -*- coding: utf-8 -*-
from hashlib import md5
import logging

logger = logging.getLogger(__name__)

from flask import render_template, session, request, redirect, url_for

from pycon.riddles import app, models, db
from pycon import stages
import sqlalchemy

def gravatar_url(email, size=16):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

app.jinja_env.filters['gravatar'] = gravatar_url

def get_user():
    email = session.get('email')
    if not email:
        return None
    return models.User.get_by_email(email)

def show_login_form(error=False, email_err=False, token_err=False, email=u''):
    return render_template('login.html', error=error, email_err=email_err, token_err=token_err, email=email)

def is_valid_email(email):
    if u'@' not in email:
        return False
    head, tail = email.split(u'@', 1)
    if len(head) < 1:
        return False
    if u'.' not in tail:
        return False
    if len(tail) < 4:
        return False
    return True

def get_token(value):
    return db.session.query(models.Token).filter(models.Token.value == value).first()

class ValidationException(ValueError):

    def __init__(self, msg, email_err=False, token_err=False):
        self.msg = msg
        self.email_err = email_err
        self.token_err = token_err

def login(email, token):
    """Attempt to login user."""
    logger.info(u'Will attempt to login user %s with token %s' % (email, token))
    if not email:
        logger.warn(u'Empty email')
        raise ValidationException(u'Email is required', email_err=True)
    if not is_valid_email(email):
        logger.warn(u'Invalid email')
        raise ValidationException(u'Invalid email', email_err=True)
    token = get_token(token)
    if not token:
        logger.warn(u'Incorrect token')
        raise ValidationException(u'Incorrect token', token_err=True)
    user = models.User.get_by_email(email)
    if not user:
        if token.is_used():
            logger.warn(u'Used token')
            raise ValidationException(u'Token already used', token_err=True)
        logger.info(u'Creating user')
        user = models.User(email=email, token_id=token.id)
        db.session.add(user)
        db.session.commit()
        first_riddle = stages.RiddlesMeta.get_by_name(app.config['FIRST_RIDDLE'])
        user.add_stage(first_riddle.name)
    else:
        logger.info(u'Existing user')
        if user.token_id != token.id:
            logger.warn(u'Non-matching token')
            raise ValidationException(u'Incorrect token', token_err=True)
        logger.info(u'Using existing user')
    return user

def logout():
    """Logout user."""
    session.pop('email', None)
    return redirect(url_for('main'))

@app.route('/', methods=['GET', 'POST'])
def main():
    # Logout support.
    if 'logout' in request.args:
        return logout()
    # Session discovery / login.
    user = get_user()
    if not user:
        if request.method == 'POST':
            email = request.form['email']
            token = request.form['token']
            try:
                user = login(email, token)
            except ValidationException, e:
                return show_login_form(error=e.msg, email_err=e.email_err, token_err=e.token_err, email=email)
            else:
                session['email'] = user.email
                return redirect(url_for('main'))
        else:
            return show_login_form()

    riddle = stages.get_riddle_for_user(user)

    if not models.Settings.is_active():
        logger.warning(u'Application is inactive')
        return render_template('inactive.html', **stages.common_ctx(user, riddle))

    tries = user.get_num_of_tries()
    max = app.config['MAX_TRIES']
    if tries >= max:
        return render_template('too_many.html', **stages.common_ctx(user, riddle))

    # Actual riddle support.
    if request.method == 'POST':
        answer = request.form['answer'] or u''
        if len(answer) > app.config['MAX_ANSWER_LENGTH']:
            return redirect(url_for('main'))
        user.add_try(answer)
        return stages.answer_riddle(user, riddle, answer)
    else:
        return stages.render_riddle(user, riddle)

def mask_email(email):
    head, tail = email.split(u'@', 1)
    return u'{0}@{1}***{2}'.format(head, tail[0], tail[-1])

@app.route('/stats', methods=['GET'])
def stats():
    query = db.session.query(
            models.User.email, sqlalchemy.func.max(models.Progress.stage), sqlalchemy.func.max(models.Progress.ts)
        ).filter(
            models.User.id == models.Progress.user_id
        ).group_by(
            models.User.email
        ).order_by(
            sqlalchemy.desc(sqlalchemy.func.max(models.Progress.stage)), sqlalchemy.func.max(models.Progress.ts)
        )
    stats = (
        (email, mask_email(email), stage, ts.strftime('%Y-%m-%d %H:%M:%S'))
        for email, stage, ts in query)
    return render_template('stats.html', stats=stats)
