# -*- coding: utf-8 -*-
"""

"""
import sys
import datetime
import logging
import string
from random import choice

logger = logging.getLogger(__name__)

from flask import redirect, url_for, render_template, current_app

class NextStage(ValueError):

    def __init__(self, stage):
        self.stage = stage

class LaterResolution(object):

    def __init__(self, name):
        self.name = name

R = LaterResolution

class RiddlesMeta(type):
    by_name = {}
    to_resolve = {}
    idx = 0
    max_idx = -1

    def __new__(meta, name, bases, attrs):
        assert name not in meta.by_name
        logger.debug(u'Registering class %s', name)
        attrs['name'] = name
        attrs['template_name'] = u'riddle_%s.html' % (name.lower(), )
        if not attrs.get('abstract', False):
            attrs['seq'] = meta.idx
            logger.debug(u'Riddle %s has idx %s', name, meta.idx)
            meta.max_idx = meta.idx
            meta.idx += 1
        for attr_name, attr_value in attrs.iteritems():
            if isinstance(attr_value, LaterResolution):
                meta.to_resolve[name, attr_name] = attr_value.name
                logger.debug(u'Will resolve %s.%s later to %s', name, attr_name, attr_value.name)
        cls = type.__new__(meta, name, bases, attrs)
        meta.by_name[name] = cls
        return cls

    @classmethod
    def resolve(meta):
        logger.debug(u'Resolving riddles')
        for (source_class_name, attr_name), target_class_name in meta.to_resolve.iteritems():
            logger.debug(u'Resolving %s.%s to %s', source_class_name, attr_name, target_class_name)
            target_class = meta.get_by_name(target_class_name)
            source_class = meta.get_by_name(source_class_name)
            setattr(source_class, attr_name, target_class)
        logger.debug(u'Riddles resolved')

    @classmethod
    def get_by_name(meta, name):
        return meta.by_name[name]

    @classmethod
    def get_total_number(meta):
        return meta.max_idx

ALLOWED_CHARS = unicode(string.letters + string.digits)

def sanitize_answer(answer):
    result = []
    for char in answer:
        if char not in ALLOWED_CHARS:
            continue
        result.append(char.lower())
    return str(u''.join(result))

class Riddle(object):
    __metaclass__ = RiddlesMeta
    abstract = True

    def render(self, msg=None, **params):
        return render_template(self.template_name, msg=msg, **params)

    def default(self, answer):
        """Return default error reply."""
        return u'Incorrect answer'

    def on_(self):
        return u'Some answer is better than no answer'

    def __call__(self, answer):
        """Try solving the puzzle with given answer."""
        method_name = 'on_%s' % sanitize_answer(answer)
        method = getattr(self, method_name, None)
        if method:
            msg = method()
        else:
            msg = self.default(answer)
        return msg

class Turing(Riddle):
    """Turing test."""

    def default(self, answer):
        return u'Death to all machines'

    def on_yes(self):
        return u"Really? I don't believe you."

    def on_tak(self):
        return u'Please reply in English'

    on_nie = on_tak

    def on_no(self):
        raise NextStage(Tomorrow)

class Tomorrow(Riddle):
    """Tomorrow."""

    DELTA = datetime.timedelta(days=1)
    NEXT_STAGE = R('Week')
    NAMES = [u'robo-brain', u'machine', u'you soulless piece of scrap metal']

    def default(self, answer):
        try:
            parsed = datetime.datetime.strptime(answer, '%Y-%m-%d').date()
        except:
            return u'Expected format is YYYY-MM-DD'
        today = datetime.date.today()
        future = today + self.DELTA
        if parsed == future:
            raise NextStage(self.NEXT_STAGE)
        else:
            return u'You are wrong, {0}!'.format(choice(self.NAMES))

class Week(Tomorrow):
    """In a week."""
    DELTA = datetime.timedelta(days=7)
    NEXT_STAGE = R('Days17')

class Days17(Week):
    """In 17 days."""
    DELTA = datetime.timedelta(days=17)
    NEXT_STAGE = R('Days2048')

class Days2048(Days17):
    """In 2048 days."""
    DELTA = datetime.timedelta(days=2048)
    NEXT_STAGE = R('Sequence')

class Sequence(Riddle):
    """Sequence (5)."""
    EXPECTED = 527
    NEXT_STAGE = R('Sequence2')

    def default(self, answer):
        try:
            answer = int(answer)
        except ValueError:
            return u'It needs to be a number'
        else:
            if answer == self.EXPECTED:
                raise NextStage(self.NEXT_STAGE)
            else:
                return u'Try again'

class Sequence2(Sequence):
    EXPECTED = 56782015046063
    NEXT_STAGE = R('Sequence3')

class Sequence3(Sequence2):
    EXPECTED = 486
    NEXT_STAGE = R('Cezar')

    def on_195480672100470143357183811948169200437932835664604768439945603963500098551334977471193440731127147509528391787(self):
        return u'Please provide just the sum of all digits'

class Cezar(Riddle):

    ANSWER = 'pieceofcake'

    def on_cvrprbspnxr(self):
        return u'Come on, show some effort'

    def on_julius(self):
        return u'We all know, this is Gaius Iulius Caesar'

    on_gaius = on_caesar = on_cezar = on_iulius = on_julius

    def default(self, answer):
        if len(answer) != len(self.ANSWER):
            return u'Output is supposed to be as long as the input'
        else:
            return u'At least the number of characters matches'

    def on_pieceofcake(self):
        raise NextStage(Imperatores)

class Imperatores(Riddle):

    def on_wdjntnozhvodnon(self):
        return u'Please input the decoded word'

    def on_biosystematists(self):
        raise NextStage(Bruteforce)

class Bruteforce(Riddle):

    def on_password(self):
        return u'Nice try, but your friend is not that stupid'

    def on_admin(self):
        return u'This would probably work on 50% of websites, but not this one'

    def on_123345678(self):
        return u'A very good guess, but this task is about breaking the encryption'

    def on_penis(self):
        return u"Yes, this is supposedly the most common password, but it's not the one we are looking for"

    def default(self, answer):
        return u"Sorry, the password you provided is not valid."

    def on_inheritor(self):
        raise NextStage(Possibilities)

class BasePossibilities(Riddle):
    abstract = True

    BASE = 10

    def default(self, answer):
        try:
            sum = int(answer, self.BASE)
        except ValueError:
            return u'Answer needs to be a number'
        else:
            return u'Incorrect answer'

class Possibilities(BasePossibilities):

    def on_133320(self):
        raise NextStage(BigPossibilities)

class BigPossibilities(BasePossibilities):

    def on_201599999798400(self):
        raise NextStage(BiggerPossibilities)

class BiggerPossibilities(BasePossibilities):

    BASE = 16

    def on_804077813274862776803112960000(self):
        return u'Please provide your answer as hexadecimal number'

    def on_a261d93ffffffff5d9e26c000(self):
        raise NextStage(BiggestPossibilities)

class BiggestPossibilities(BasePossibilities):

    BASE = 36

    def on_8675655607006888374539099777013298505261910478828726567754098829152300097863680000000(self):
        return u'Please provide your answer as base-36 number'

    def on_477418825e75f0e81cd4fe3452114d99200c5dc0ffe45116dae4cfadb723722c4000000(self):
        return u'Hexadecimal numbers were expected in the previous riddle, use base-36'

    def on_7wmf7oufq8qy3da7zzzzzzzzzzzzzzzzs3dksb5k9r91wmps0000000(self):
        raise NextStage(Final)

class Final(Riddle):

    def default(self, answer):
        return u"You are at the journey's end"

class Unknown(Riddle):
    pass


RiddlesMeta.resolve()


def common_ctx(user, riddle):
    progress = user.get_progress()
    stage = progress.stage
    tries = user.get_num_of_tries()
    max_tries = current_app.config['MAX_TRIES']
    max_answer_length = current_app.config['MAX_ANSWER_LENGTH']
    email = user.email
    total_riddles = RiddlesMeta.get_total_number()
    current_riddle = riddle.seq + 1
    return {
        'progress': progress,
        'stage': stage,
        'tries': tries,
        'max_tries': max_tries,
        'total_riddles': total_riddles,
        'current_riddle': current_riddle,
        'max_answer_length': max_answer_length,
        'email': email
    }


def get_riddle_for_user(user):
    progress = user.get_progress()
    stage = progress.stage
    logger.debug(u'Getting riddle %s for user %s', stage, user.email)
    Riddle = RiddlesMeta.get_by_name(stage)
    riddle = Riddle()
    return riddle


def render_riddle(user, riddle):
    return riddle.render(**common_ctx(user, riddle))


def answer_riddle(user, riddle, answer):
    stage = riddle.name
    try:
        msg = riddle(answer)
    except NextStage, e:
        next_stage = e.stage
        logger.info(u'User %s advances from stage %s to stage %s thanks to answer %s',
            user.email, stage, next_stage, answer)
        user.add_stage(next_stage.name)
        return redirect(url_for('main'))
    else:
        logger.info(u'User %s gave wrong answer %s at stage %s', user.email, answer, stage)
        return riddle.render(msg=msg, answer=answer, **common_ctx(user, riddle))
