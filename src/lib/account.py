from flask import session, current_app, flash

from ..internals.database.database import get_cursor
from ..utils.utils import get_value
from ..internals.cache.redis import get_conn
from ..lib.favorites import add_favorite_artist
from ..lib.artist import get_artist
from ..lib.security import is_login_rate_limited

import ujson
import copy
import bcrypt
import base64
import hashlib
import dateutil
from threading import Lock
from bleach.sanitizer import Cleaner

account_create_lock = Lock()

def load_account(account_id = None, reload = False):
    if account_id is None and 'account_id' in session:
        return load_account(session['account_id'], reload)
    elif account_id is None and 'account_id' not in session:
        return None

    redis = get_conn()
    key = 'account:' + str(account_id)
    account = redis.get(key)
    if account is None or reload:
        cursor = get_cursor()
        query = 'select id, username, created_at from account where id = %s'
        cursor.execute(query, (account_id,))
        account = cursor.fetchone()
        redis.set(key, serialize_account(account))
    else:
        account = deserialize_account(account)

    return account

def get_login_info_for_username(username):
    cursor = get_cursor()
    query = 'select id, password_hash from account where username = %s'
    cursor.execute(query, (username,))
    return cursor.fetchone()

def is_logged_in():
    if 'account_id' in session:
        return True
    return False

def is_username_taken(username):
    cursor = get_cursor()
    query = 'select id from account where username = %s'
    cursor.execute(query, (username,))
    return cursor.fetchone() is not None

def create_account(username, password, favorites):
    account_id = None
    password_hash = bcrypt.hashpw(get_base_password_hash(password), bcrypt.gensalt()).decode('utf-8')
    account_create_lock.acquire()
    try:
        if is_username_taken(username):
            return False

        scrub = Cleaner(tags = [])

        cursor = get_cursor()
        query = "insert into account (username, password_hash) values (%s, %s) returning id"
        cursor.execute(query, (scrub.clean(username), password_hash,))
        account_id = cursor.fetchone()['id']
    finally:
        account_create_lock.release()

    if favorites is not None:
        for favorite in favorites:
            artist = get_artist(favorite['service'], favorite['artist_id'])
            if artist is None:
                continue
            add_favorite_artist(account_id, favorite['service'], favorite['artist_id'])

    return True

def attempt_login(username, password):
    if username is None or password is None:
        return False

    account_info = get_login_info_for_username(username)
    if account_info is None:
        flash('Username or password is incorrect')
        return False

    if get_value(current_app.config, 'ENABLE_LOGIN_RATE_LIMITING') and is_login_rate_limited(account_info['id']):
        flash('You\'re doing that too much. Try again in a little bit.')
        return False

    if bcrypt.checkpw(get_base_password_hash(password), account_info['password_hash'].encode('utf-8')):
        account = load_account(account_info['id'], True)
        session['account_id'] = account['id']
        return True

    flash('Username or password is incorrect')
    return False

def get_base_password_hash(password):
    return base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())

def serialize_account(account):
    account = copy.deepcopy(account)
    return ujson.dumps(prepare_account_fields(account))

def deserialize_account(account):
    account = ujson.loads(account)
    return rebuild_account_fields(account)

def prepare_account_fields(account):
    account['created_at'] = account['created_at'].isoformat()
    return account

def rebuild_account_fields(account):
    account['created_at'] = dateutil.parser.parse(account['created_at'])
    return account
