from flask import Blueprint, render_template, make_response

help_app = Blueprint('help_app', __name__)
@help_app.route('/')
def help():
    props = {
        'currentPage': 'help'
    }
    response = make_response(render_template(
        'help_list.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@help_app.route('/posts')
def posts():
    props = {
        'currentPage': 'help'
    }
    response = make_response(render_template(
        'help_posts.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@help_app.route('/about')
def about():
    props = {
        'currentPage': 'help'
    }
    response = make_response(render_template(
        'about.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@help_app.route('/bans')
def bans():
    props = {
        'currentPage': 'help'
    }
    response = make_response(render_template(
        'bans.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@help_app.route('/license')
def license():
    props = {
        'currentPage': 'help'
    }
    response = make_response(render_template(
        'license.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@help_app.route('/rules')
def rules():
    props = {
        'currentPage': 'help'
    }
    response = make_response(render_template(
        'rules.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response