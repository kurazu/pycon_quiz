import os
import sys
import logging.config

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
app.config.from_object(os.environ['RIDDLES_CONFIG'])
logging.config.fileConfig(app.config['LOGGING_CONFIG_FILE'])
db = SQLAlchemy(app)

from pycon import models
from pycon import views

def run():
    app.run(host=app.config['HOST'])

def init_db():
    db.create_all()

def gen_tokens():
    num = int(sys.argv[1])
    for i in xrange(num):
        token = models.Token.generate()
        print i, token.value
        db.session.add(token)
    db.session.commit()

def free_tokens():
    query = db.session.query(
        models.Token
    ).filter(
        ~sqlalchemy.exists(
        ).where(
            models.Token.id == models.User.token_id
        )
    ).order_by(
        models.Token.id
    )
    for i, token in enumerate(query):
        print i, token.value

if __name__ == '__main__':
    run()
