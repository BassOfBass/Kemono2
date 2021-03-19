TODO: write actual README
## Setup
### With Docker
```sh
# cd to kemono directory
cp .env.example .env # open .env and configure
cp flask.cfg.example flask.cfg # open flask.cfg and configure
cp kitsune.py.example kitsune.py # open kitsune.py and configure
docker-compose build
docker-compose up -d
```
### Manually
This assumes you have Python 3 installed and a running PostgreSQL server.
```sh
# make sure your database is initialized
# cd to kemono directory
pip install virtualenv
virtualenv venv
source venv/bin/activate # venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env # open .env and configure
cp flask.cfg.example flask.cfg # open flask.cfg and configure
set FLASK_APP=server.py
set FLASK_ENV=development
flask run
```