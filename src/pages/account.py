from flask import Blueprint, request, make_response, render_template, session, redirect, flash, url_for, current_app

import urllib
import json

from ..utils.utils import make_cache_key, get_value
from ..lib.account import load_account, is_username_taken, attempt_login, create_account
from ..lib.security import is_password_compromised
from ..internals.cache.flask_cache import cache

account = Blueprint('account', __name__)

@account.route('/account/login', methods=['GET'])
def get_login():
    props = {
        'currentPage': 'login',
        'query_string': ''
    }

    account = load_account()
    if account is not None:
        return redirect(url_for('artists.list'))

    query = request.query_string.decode('utf-8')
    if len(query) > 0:
        props['query_string'] = '?' + query

    response = make_response(render_template(
        'login.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

@account.route('/account/login', methods=['POST'])
def post_login():
    account = load_account()
    if account is not None:
        return redirect(url_for('artists.list'))

    query = request.query_string.decode('utf-8')
    if len(query) > 0:
        query = '?' + query

    username = get_value(request.form, 'username')
    password = get_value(request.form, 'password')
    success = attempt_login(username, password)
    if not success:
        return redirect(url_for('account.get_login') +  query)

    redir = get_value(request.args, 'redir')
    if redir is not None:
        return redirect(redir)

    return redirect(url_for('artists.list'))

@account.route('/account/logout')
def logout():
    if 'account_id' in session:
        session.pop('account_id')
    return redirect(url_for('artists.list'))

@account.route('/account/register', methods=['GET'])
def get_register():
    props = {
        'currentPage': 'login',
        'query_string': ''
    }

    account = load_account()
    if account is not None:
        return redirect(url_for('artists.list'))

    query = request.query_string.decode('utf-8')
    if len(query) > 0:
        props['query_string'] = '?' + query

    return make_response(render_template(
        'register.html',
        props = props
    ), 200)

@account.route('/account/register', methods=['POST'])
def post_register():
    props = {
        'query_string': ''
    }

    query = request.query_string.decode('utf-8')
    if len(query) > 0:
        props['query_string'] = '?' + query

    username = get_value(request.form, 'username')
    password = get_value(request.form, 'password')
    favorites_json = get_value(request.form, 'favorites', '[]')
    confirm_password = get_value(request.form, 'confirm_password')

    favorites = []
    if favorites_json != '':
        favorites = json.loads(favorites_json)

    errors = False
    if username.strip() == '':
        flash('Username cannot be empty')
        errors = True

    if password.strip() == '':
        flash('Password cannot be empty')
        errors = True

    if password != confirm_password:
        flash('Passwords do not match')
        errors = True

    if is_username_taken(username):
        flash('Username already taken')
        errors = True

    if get_value(current_app.config, 'ENABLE_PASSWORD_VALIDATOR') and is_password_compromised(password):
        flash('We\'ve detected that password was compromised in a data breach on another site. Please choose a different password.')
        errors = True

    if not errors:
        success = create_account(username, password, favorites)
        if not success:
            flash('Username already taken')
            errors = True

    if not errors:
        account = attempt_login(username, password)
        if account is None:
            current_app.logger.warning("Error logging into account immediately after creation")
        flash('Account created successfully')

        redir = get_value(request.args, 'redir')
        if redir is not None:
            return redirect(redir)

        return redirect(url_for('artists.list'))

    return make_response(render_template(
        'register.html',
        props = props
    ), 200)

@account.route('/account')
def get_account():
    account = load_account()
    if account is None:
        return redirect(url_for('account.get_login'))

    return make_response(render_template(
        'account.html',
        props = {}
    ), 200)
