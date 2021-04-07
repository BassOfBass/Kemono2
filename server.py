import re
from os import getenv, stat, rename, makedirs
from os.path import join, dirname, isfile, splitext
from shutil import move
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

import src.internals.database.database as database
import src.internals.cache.redis as redis
from src.internals.cache.flask_cache import cache
from src.lib.ab_test import get_all_variants
from src.lib.account import is_logged_in
from src.utils.utils import url_is_for_non_logged_file_extension

from src.pages.home import home
from src.pages.legacy import legacy
from src.pages.artists import artists
from src.pages.random import random
from src.pages.post import post
from src.pages.account import account
from src.pages.favorites import favorites
from src.pages.help import help_app
from src.pages.proxy import proxy_app

app = Flask(
    __name__,
    template_folder='views'
)
<<<<<<< HEAD
app.config.from_pyfile('flask.cfg')
cache = Cache(app)
app.url_map.strict_slashes = False
app.jinja_env.filters['regex_match'] = lambda val, rgx: re.search(rgx, val)
app.jinja_env.filters['regex_find'] = lambda val, rgx: re.findall(rgx, val)
app.register_blueprint(help_app, url_prefix='/help')
app.register_blueprint(proxy_app, url_prefix='/proxy')
try:
    pool = psycopg2.pool.SimpleConnectionPool(1, 20,
        host = getenv('PGHOST') if getenv('PGHOST') else 'localhost',
        dbname = getenv('PGDATABASE') if getenv('PGDATABASE') else 'kemonodb',
        user = getenv('PGUSER') if getenv('PGUSER') else 'nano',
        password = getenv('PGPASSWORD') if getenv('PGPASSWORD') else 'shinonome',
        cursor_factory = RealDictCursor
    )
except Exception as error:
    print("Failed to connect to the database: ",error)
=======

app.url_map.strict_slashes = False

app.register_blueprint(home)
app.register_blueprint(legacy)
app.register_blueprint(artists)
app.register_blueprint(random)
app.register_blueprint(post)
app.register_blueprint(account)
app.register_blueprint(favorites)
app.register_blueprint(help_app, url_prefix='/help')
app.register_blueprint(proxy_app, url_prefix='/proxy')

app.config.from_pyfile('flask.cfg')
app.jinja_env.globals.update(is_logged_in=is_logged_in)
app.jinja_env.filters['regex_match'] = lambda val, rgx: re.search(rgx, val)
app.jinja_env.filters['regex_find'] = lambda val, rgx: re.findall(rgx, val)

logging.basicConfig(filename='kemono.log', level=logging.DEBUG)
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)
>>>>>>> root/master

def make_cache_key(*args,**kwargs):
    return request.full_path

@app.before_request
<<<<<<< HEAD
def clear_trailing():
    rp = request.path
    if rp != '/' and rp.endswith('/'):
        response = redirect(rp[:-1])
        response.autocorrect_location_header = False
        return response

def get_cursor():
    if 'cursor' not in g:
        g.connection = pool.getconn()
        g.cursor = g.connection.cursor()
    return g.cursor

def allowed_file(mime, accepted):
    return any(x in mime for x in accepted)
=======
def do_init_stuff():
    g.request_start_time = datetime.datetime.now()
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=9999)
    session.modified = False

@app.after_request
def do_finish_stuff(response):
    if not url_is_for_non_logged_file_extension(request.path):
        start_time = g.request_start_time
        end_time = datetime.datetime.now()
        elapsed = end_time - start_time
        app.logger.debug('[{4}] Completed {0} request to {1} in {2}ms with ab test variants: {3}'.format(request.method, request.url, elapsed.microseconds/1000, get_all_variants(), end_time.strftime("%Y-%m-%d %X")))
    response.autocorrect_location_header = False
    return response
>>>>>>> root/master

@app.errorhandler(413)
def upload_exceeded(error):
    props = {
        'redirect': request.args.get('Referer') if request.args.get('Referer') else '/'
    }
    limit = int(getenv('REQUESTS_IMAGES')) if getenv('REQUESTS_IMAGES') else 1048576
    props['message'] = 'Submitted file exceeds the upload limit. {} MB for requests images.'.format(
        limit / 1024 / 1024
    )
    return render_template(
        'error.html',
        props = props
    ), 413

@app.teardown_appcontext
def close(e):
    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()
        connection = g.pop('connection', None)
        if connection is not None:
            connection.commit()
            pool.putconn(connection)

@app.route('/')
@cache.cached(key_prefix=make_cache_key)
def artists():
    props = {
        'currentPage': 'artists'
    }
    base = request.args.to_dict()
    base.pop('o', None)
    if not request.args.get('commit'):
        results = {}
    else:
        query = "SELECT * FROM lookup "
        query += "WHERE name ILIKE %s "
        params = ('%' + request.args.get('q') + '%',)
        if request.args.get('service'):
            query += "AND service = %s "
            params += (request.args.get('service'),)
        query += "AND service != 'discord-channel' "
        query += "ORDER BY " + {
            'indexed': 'indexed',
            'name': 'name',
            'service': 'service'
        }.get(request.args.get('sort_by'), 'indexed')
        query += {
            'asc': ' asc ',
            'desc': ' desc '
        }.get(request.args.get('order'), 'asc')
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params += (offset,)
        query += "LIMIT 25"

        cursor = get_cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
    response = make_response(render_template(
        'artists.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/artists')
def root():
    response = redirect('/', code=308)
    response.autocorrect_location_header = False
    return response

@app.route('/thumbnail/<path:path>')
def thumbnail(path):
    try:
        image = Image.open(join(getenv('DB_ROOT'), path))
        image = image.convert('RGB')
        image.thumbnail((800, 800))
        makedirs(dirname(join(getenv('DB_ROOT'), 'thumbnail', path)), exist_ok=True)
        image.save(join(getenv('DB_ROOT'), 'thumbnail', path), 'JPEG', quality=60)
        response = redirect(join('/', 'thumbnail', path), code=302)
        response.autocorrect_location_header = False
        return response
    except Exception as e:
        return f"The file you requested could not be converted. Error: {e}", 404

@app.route('/artists/random')
def random_artist():
    cursor = get_cursor()
    query = "SELECT id, service FROM lookup WHERE service != 'discord-channel' ORDER BY random() LIMIT 1"
    cursor.execute(query)
    random = cursor.fetchall()
    if len(random) == 0:
        return redirect('back')
    response = redirect(url_for('user', service = random[0]['service'], id = random[0]['id']))
    response.autocorrect_location_header = False
    return response

@app.route('/artists/updated')
@cache.cached(key_prefix=make_cache_key)
def updated_artists():
    cursor = get_cursor()
    props = {
        'currentPage': 'artists'
    }
    query = 'WITH "posts" as (select "user", "service", max("added") from "posts" group by "user", "service" order by max(added) desc limit 50) '\
        'select "user", "posts"."service" as service, "lookup"."name" as name, "max" from "posts" inner join "lookup" on "posts"."user" = "lookup"."id"'
    cursor.execute(query)
    results = cursor.fetchall()
    response = make_response(render_template(
        'updated.html',
        props = props,
        results = results
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/artists/favorites')
def favorites():
    props = {
        'currentPage': 'artists'
    }
    response = make_response(render_template(
        'favorites.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=300, public, stale-while-revalidate=2592000'
    return response

@app.route('/posts')
@cache.cached(key_prefix=make_cache_key)
def posts():
    cursor = get_cursor()
    props = {
        'currentPage': 'posts'
    }
    base = request.args.to_dict()
    base.pop('o', None)

    query = "SELECT * FROM posts ORDER BY added desc "
    params = ()

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and request.args.get('limit') <= 50 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    response = make_response(render_template(
        'posts.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/posts/upload')
def upload_post():
    props = {
        'currentPage': 'posts'
    }
    response = make_response(render_template(
        'upload.html',
        props=props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/posts/random')
def random_post():
    cursor = get_cursor()
    query = "SELECT service, \"user\", id FROM posts WHERE random() < 0.01 LIMIT 1"
    cursor.execute(query)
    random = cursor.fetchall()
    response = redirect(url_for('post', service = random[0]['service'], id = random[0]['user'], post = random[0]['id']))
    response.autocorrect_location_header = False
    return response

# TODO: /:service/user/:id/rss

@app.route('/<service>/user/<id>')
@cache.cached(key_prefix=make_cache_key)
def user(service, id):
    cursor = get_cursor()
    props = {
        'currentPage': 'posts',
        'id': id,
        'service': service
    }
    base = request.args.to_dict()
    base.pop('o', None)
    base["service"] = service
    base["id"] = id

    query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s ORDER BY published desc "
    params = (id, service)

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 50 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor2 = get_cursor()
    query2 = "SELECT id FROM posts WHERE \"user\" = %s AND service = %s GROUP BY id"
    params2 = (id, service)
    cursor2.execute(query2, params2)
    results2 = cursor2.fetchall()
    props["count"] = len(results2)

    response = make_response(render_template(
        'user.html',
        props = props,
        results = results,
        base = base
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/discord/server/<id>')
def discord_server(id):
    response = make_response(render_template(
        'discord.html'
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/<service>/user/<id>/post/<post>')
@cache.cached(key_prefix=make_cache_key)
def post(service, id, post):
    cursor = get_cursor()
    props = {
        'currentPage': 'posts',
        'service': service if service else 'patreon'
    }
    query = 'SELECT * FROM posts '
    query += 'WHERE id = %s '
    params = (post,)
    query += 'AND posts.user = %s '
    params += (id,)
    query += 'AND service = %s '
    params += (service,)
    query += 'ORDER BY added asc'

    cursor.execute(query, params)
    results = cursor.fetchall()

    result_previews = []
    result_attachments = []
    for post in results:
        previews = []
        attachments = []
        if len(post['file']):
            if re.search("\.(gif|jpe?g|jpe|png|webp)$", post['file']['path'], re.IGNORECASE):
                previews.append({
                    'type': 'thumbnail',
                    'path': post['file']['path'].replace('https://kemono.party','')
                })
            else:
                attachments.append({
                    'path': post['file']['path'],
                    'name': post['file'].get('name')
                })
        if len(post['embed']):
            previews.append({
                'type': 'embed',
                'url': post['embed']['url'],
                'subject': post['embed']['subject'],
                'description': post['embed']['description']
            })
        for attachment in post['attachments']:
            if re.search("\.(gif|jpe?g|jpe|png|webp)$", attachment['path'], re.IGNORECASE):
                previews.append({
                    'type': 'thumbnail',
                    'path': attachment['path'].replace('https://kemono.party','')
                })
            else:
                attachments.append({
                    'path': attachment['path'],
                    'name': attachment['name']
                })
        result_previews.append(previews)
        result_attachments.append(attachments)
    
    props['posts'] = results[0]
    response = make_response(render_template(
        'post.html',
        props = props,
        results = results,
        result_previews = result_previews,
        result_attachments = result_attachments
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/board')
def board():
    props = {
        'currentPage': 'board'
    }
    response = make_response(render_template(
        'board_list.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/requests')
def requests_list():
    props = {
        'currentPage': 'requests'
    }
    base = request.args.to_dict()
    base.pop('o', None)

    if not request.args.get('commit'):
        query = "SELECT * FROM requests "
        query += "WHERE status = 'open' "
        query += "ORDER BY votes desc "
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params = (offset,)
        query += "LIMIT 25"
    else:
        query = "SELECT * FROM requests "
        query += "WHERE title ILIKE %s "
        params = ('%' + request.args.get('q') + '%',)
        if request.args.get('service'):
            query += "AND service = %s "
            params += (request.args.get('service'),)
        query += "AND service != 'discord' "
        if request.args.get('max_price'):
            query += "AND price <= %s "
            params += (request.args.get('max_price'),)
        query += "AND status = %s "
        params += (request.args.get('status'),)
        query += "ORDER BY " + {
            'votes': 'votes',
            'created': 'created',
            'price': 'price'
        }.get(request.args.get('sort_by'), 'votes')
        query += {
            'asc': ' asc ',
            'desc': ' desc '
        }.get(request.args.get('order'), 'desc')
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params += (offset,)
        query += "LIMIT 25"

    cursor = get_cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()

    response = make_response(render_template(
        'requests_list.html',
        props = props,
        results = results,
        base = base
    ), 200)
    return response

@app.route('/requests/<id>/vote_up', methods=['POST'])
def vote_up(id):
    ip = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1] if 'X-Forwarded-For' in request.headers else request.remote_addr
    query = "SELECT * FROM requests WHERE id = %s"
    params = (id,)

    cursor = get_cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()

    props = {
        'currentPage': 'requests',
        'redirect': request.args.get('Referer') if request.args.get('Referer') else '/requests'
    }

    if not len(result):
        abort(404)
    hash = sha256(ip.encode()).hexdigest()
    if hash in result.get('ips'):
        props['message'] = 'You already voted on this request.'
        return make_response(render_template(
            'error.html',
            props = props
        ), 401)
    else:
        record = result.get('ips')
        record.append(hash)
        query = "UPDATE requests SET votes = votes + 1,"
        query += "ips = %s "
        params = (record,)
        query += "WHERE id = %s"
        params += (id,)
        cursor.execute(query, params)

        return make_response(render_template(
            'success.html',
            props = props
        ), 200)

@app.route('/requests/new')
def request_form():
    props = {
        'currentPage': 'requests'
    }

    response = make_response(render_template(
        'requests_new.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/requests/new', methods=['POST'])
def request_submit():
    props = {
        'currentPage': 'requests',
        'redirect': request.args.get('Referer') if request.args.get('Referer') else '/requests'
    }

    ip = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1] if 'X-Forwarded-For' in request.headers else request.remote_addr

    if not request.form.get('user_id'):
        props['message'] = 'You didn\'t enter a user ID.'
        return make_response(render_template(
            'error.html',
            props = props
        ), 400)

    if getenv('TELEGRAMTOKEN'):
        snippet = ''
        with open('views/requests_new.html', 'r') as file:
            snippet = file.read()

        requests.post(
            'https://api.telegram.org/bot' + getenv('TELEGRAMTOKEN') + '/sendMessage',
            params = {
                'chat_id': '-' + getenv('TELEGRAMCHANNEL'),
                'parse_mode': 'HTML',
                'text': render_template_string(snippet)
            }
        )

    filename = ''
    try:
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename and allowed_file(image.content_type, ['png', 'jpeg', 'gif']):
                filename = original = slugify_filename(secure_filename(image.filename))
                tmp = join('/tmp', filename)
                image.save(tmp)
                limit = int(getenv('REQUESTS_IMAGES')) if getenv('REQUESTS_IMAGES') else 1048576
                if stat(tmp).st_size > limit:
                    abort(413)
                makedirs(join(getenv('DB_ROOT'), 'requests', 'images'), exist_ok=True)
                store = join(getenv('DB_ROOT'), 'requests', 'images', filename)
                copy = 1
                while isfile(store):
                    filename = splitext(original)[0] + '-' + str(copy) + splitext(original)[1]
                    store = join(getenv('DB_ROOT'), 'requests', 'images', filename)
                    copy += 1
                move(tmp, store)
    except Exception as error:
        props['message'] = 'Failed to upload image. Error: {}'.format(error)
        return make_response(render_template(
            'error.html',
            props = props
        ), 500)

    scrub = Cleaner(tags = [])
    text = Cleaner(tags = ['br'])

    columns = ['service','"user"','title','description','price','ips']
    description = request.form.get('description').strip().replace('\n', '<br>\n')
    params = (
        scrub.clean(request.form.get('service')),
        scrub.clean(request.form.get('user_id').strip()),
        scrub.clean(request.form.get('title').strip()),
        text.clean(description),
        scrub.clean(request.form.get('price').strip()),
        [sha256(ip.encode()).hexdigest()]
    )
    if request.form.get('specific_id'):
        columns.append('post_id')
        params += (scrub.clean(request.form.get('specific_id').strip()),)
    if filename:
        columns.append('image')
        params += (join('/requests', 'images', filename),)
    data = ['%s'] * len(params)

    query = "INSERT INTO requests ({fields}) VALUES ({values})".format(
        fields = ','.join(columns),
        values = ','.join(data)
    )

    cursor = get_cursor()
    cursor.execute(query, params)

    return make_response(render_template(
        'success.html',
        props = props
    ), 200)

@app.route('/importer')
def importer():
    props = {
        'currentPage': 'import'
    }

    response = make_response(render_template(
        'importer_list.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/importer/tutorial')
def importer_tutorial():
    props = {
        'currentPage': 'import'
    }

    response = make_response(render_template(
        'importer_tutorial.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/importer/ok')
def importer_ok():
    props = {
        'currentPage': 'import'
    }

    response = make_response(render_template(
        'importer_ok.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/importer/status/<lgid>')
def importer_status(lgid):
    props = {
        'currentPage': 'import',
        'id': lgid
    }

    try:
        with open(join(getenv('DB_ROOT'), 'logs', lgid + '.log')) as f:
            response = make_response(render_template(
                'importer_status.html',
                props = props,
                log = f.read()
            ), 200)
    except IOError:
        props['message'] = 'That log doesn\'t exist.'
        response = make_response(render_template(
            'error.html',
            props = props
        ), 401)

    response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'
    return response

### API ###
@app.route('/api/import', methods=['POST'])
def importer_submit():
    host = getenv('ARCHIVERHOST')
    port = getenv('ARCHIVERPORT') if getenv('ARCHIVERPORT') else '8000'

    try:
        r = requests.post(
            f'http://{host}:{port}/api/import',
            json = {
                'service': request.form.get("service"),
                'session_key': request.form.get("session_key"),
                'channel_ids': request.form.get("channel_ids")
            },
            params = {
                'service': request.form.get("service"),
                'session_key': request.form.get("session_key"),
                'channel_ids': request.form.get("channel_ids")
            }
        )
        r.raise_for_status()
        # in new importer, return just the id instead of a whole page
        props = {
            'currentPage': 'import',
            'redirect': f'/importer/status/{r.text}'
        }
        return make_response(render_template(
            'success.html',
            props = props
        ), 200)
    except Exception as e:
        return f'Error while connecting to archiver. Is it running? Error: {e}', 500
    
# TODO: file sharing api (/api/upload)

@app.route('/api/bans')
def bans():
    cursor = get_cursor()
    query = "SELECT * FROM dnp"
    cursor.execute(query)
    results = cursor.fetchall()
    return make_response(jsonify(results), 200)

@app.route('/api/recent')
def recent():
    cursor = get_cursor()
    query = "SELECT * FROM posts ORDER BY added desc "
    params = ()

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 50 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    response = make_response(jsonify(results), 200)
    response.headers['Cache-Control'] = 'max-age=60, public, stale-while-revalidate=2592000'
    return response

@app.route('/api/lookup')
def lookup():
    if (request.args.get('q') is None):
        return make_response('Bad request', 400)
    cursor = get_cursor()
    query = "SELECT * FROM lookup "
    params = ()
    query += "WHERE name ILIKE %s "
    params += ('%' + request.args.get('q') + '%',)
    if (request.args.get('service')):
        query += "AND service = %s "
        params += (request.args.get('service'),)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 150 else 50
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()
    response = make_response(jsonify(list(map(lambda x: x['id'], results))), 200)
    return response

@app.route('/api/discord/channels/lookup')
def discord_lookup():
    cursor = get_cursor()
    query = "SELECT channel FROM discord_posts WHERE server = %s GROUP BY channel"
    params = (request.args.get('q'),)
    cursor.execute(query, params)
    channels = cursor.fetchall()
    lookup = []
    for x in channels:
        cursor = get_cursor()
        cursor.execute("SELECT * FROM lookup WHERE service = 'discord-channel' AND id = %s", (x['channel'],))
        lookup_result = cursor.fetchall()
        lookup.append({ 'id': x['channel'], 'name': lookup_result[0]['name'] if len(lookup_result) else '' })
    response = make_response(jsonify(lookup))
    return response

@app.route('/api/discord/channel/<id>')
def discord_channel(id):
    cursor = get_cursor()
    query = "SELECT * FROM discord_posts WHERE channel = %s ORDER BY published desc "
    params = (id,)

    offset = request.args.get('skip') if request.args.get('skip') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 150 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()
    return jsonify(results)

@app.route('/api/lookup/cache/<id>')
def lookup_cache(id):
    if (request.args.get('service') is None):
        return make_response('Bad request', 400)
    cursor = get_cursor()
    query = "SELECT * FROM lookup WHERE id = %s AND service = %s"
    params = (id, request.args.get('service'))
    cursor.execute(query, params)
    results = cursor.fetchall()
    response = make_response(jsonify({ "name": results[0]['name'] if len(results) > 0 else '' }))
    return response

@app.route('/api/<service>/user/<user>/lookup')
def user_search(service, user):
    if (request.args.get('q') and len(request.args.get('q')) > 35):
        return make_response('Bad request', 400)
    cursor = get_cursor()
    query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s "
    params = (user, service)
    query += "AND to_tsvector(content || ' ' || title) @@ websearch_to_tsquery(%s) "
    params += (request.args.get('q'),)
    query += "ORDER BY published desc "

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 150 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()
    return jsonify(results)

@app.route('/api/<service>/user/<user>/post/<post>')
def post_api(service, user, post):
    cursor = get_cursor()
    query = "SELECT * FROM posts WHERE id = %s AND \"user\" = %s AND service = %s ORDER BY added asc"
    params = (post, user, service)
    cursor.execute(query, params)
    results = cursor.fetchall()
    print(results)
    return jsonify(results)

@app.route('/api/<service>/user/<user>/post/<post>/flag')
def flag_api(service, user, post):
    cursor = get_cursor()
    query = "SELECT * FROM booru_flags WHERE id = %s AND \"user\" = %s AND service = %s"
    params = (post, user, service)
    cursor.execute(query, params)
    results = cursor.fetchall()
    return "", 200 if len(results) else 404

@app.route('/api/<service>/user/<user>/post/<post>/flag', methods=["POST"])
def new_flag_api(service, user, post):
    cursor = get_cursor()
    query = "SELECT * FROM posts WHERE id = %s AND \"user\" = %s AND service = %s"
    params = (post, user, service)
    cursor.execute(query, params)
    results = cursor.fetchall()
    if len(results) == 0:
        return "", 404
    
    cursor2 = get_cursor()
    query2 = "SELECT * FROM booru_flags WHERE id = %s AND \"user\" = %s AND service = %s"
    params2 = (post, user, service)
    cursor2.execute(query2, params2)
    results2 = cursor.fetchall()
    if len(results2) > 0:
        # conflict; flag already exists
        return "", 409
    
    scrub = Cleaner(tags = [])
    columns = ['id','"user"','service']
    params = (
        scrub.clean(post),
        scrub.clean(user),
        scrub.clean(service)
    )
    data = ['%s'] * len(params)
    query = "INSERT INTO booru_flags ({fields}) VALUES ({values})".format(
        fields = ','.join(columns),
        values = ','.join(data)
    )
    cursor3 = get_cursor()
    cursor3.execute(query, params)

    return "", 200

@app.route('/api/<service>/user/<id>')
@cache.cached(key_prefix=make_cache_key)
def user_api(service, id):
    cursor = get_cursor()
    query = "SELECT * FROM posts WHERE \"user\" = %s AND service = %s ORDER BY published desc "
    params = (id, service)

    offset = request.args.get('o') if request.args.get('o') else 0
    query += "OFFSET %s "
    params += (offset,)
    limit = request.args.get('limit') if request.args.get('limit') and int(request.args.get('limit')) <= 50 else 25
    query += "LIMIT %s"
    params += (limit,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    return jsonify(results)