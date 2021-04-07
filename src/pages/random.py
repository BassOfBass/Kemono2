from flask import Blueprint, redirect, url_for, g

from ..utils.utils import make_cache_key
from ..internals.cache.redis import get_conn
from ..internals.cache.flask_cache import cache
from ..internals.database.database import get_cursor

from ..lib.artist import get_artist, get_random_artist_keys
from ..lib.post import get_post, get_random_posts_keys
from ..lib.ab_test import get_ab_variant
from ..utils.utils import get_value

import random as rand

random = Blueprint('random', __name__)

@random.route('/posts/random')
def random_post():
    post = get_random_post()
    if post is None:
        return redirect('back')

    return redirect(url_for('post.get', service = post['service'], artist_id = post['user'], post_id = post['id']))

@random.route('/artists/random')
def random_artist():
    artist = get_random_artist()
    if artist is None:
        return redirect('back')

    return redirect(url_for('artists.get', service = artist['service'], artist_id = artist['id']))

def get_random_post():
    post_keys = get_random_posts_keys(1000)
    if len(post_keys) == 0:
        return None
    return rand.choice(post_keys)

def get_random_artist():
    artists = get_random_artist_keys(1000)
    if len(artists) == 0:
        return None
    return rand.choice(artists)
