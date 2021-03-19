import re
import cloudscraper
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify, render_template, make_response

proxy_app = Blueprint('proxy', __name__, template_folder='../views')
@proxy_app.route('/patreon/user/<id>')
def patreon(id):
  scraper = cloudscraper.create_scraper()
  data = scraper.get('https://www.patreon.com/api/user/' + id).json()
  response = make_response(jsonify(data), 200)
  response.headers['Cache-Control'] = 'max-age=2629800, public, stale-while-revalidate=2592000'
  return response

@proxy_app.route('/fanbox/user/<id>')
def fanbox(id):
  data = requests.get('https://api.fanbox.cc/creator.get?userId=' + id, headers={"origin":"https://fanbox.cc"}).json()
  response = make_response(jsonify(data), 200)
  response.headers['Cache-Control'] = 'max-age=2629800, public, stale-while-revalidate=2592000'
  return response

@proxy_app.route('/gumroad/user/<id>')
def gumroad(id):
  data = requests.get('https://gumroad.com/' + id).text
  soup = BeautifulSoup(data, 'html.parser')
  try:
    response = make_response(jsonify({
      # "background": soup.find('img', class_='profile-background-container js-background-image-container')['src'],
      "avatar": re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpe?g|gif)', soup.find('div', class_='profile-picture js-profile-picture')['style'], re.IGNORECASE)[0],
      "name": soup.find('h2', class_='creator-profile-card__name js-creator-name').string.replace("\n", "")
    }), 200)
  except Exception as error:
    print('Failed to get Gumroad data for user {0}. '.format(id), error)
    response = make_response(
      'Failed to get Gumroad data for user {0}.'.format(id),
      500
    )
    response.mimetype = 'text/plain'
    return response
  response.headers['Cache-Control'] = 'max-age=2629800, public, stale-while-revalidate=2592000'
  return response

@proxy_app.route('/subscribestar/user/<id>')
def subscribestar(id):
  data = requests.get('https://subscribestar.adult/' + id).text
  soup = BeautifulSoup(data, 'html.parser')
  response = make_response(jsonify({
    "background": soup.find('img', class_='profile_main_info-cover')['src'],
    "avatar": soup.find('div', class_='profile_main_info-userpic').contents[0]['src'],
    "name": soup.find('div', class_='profile_main_info-name').string
  }), 200)
  response.headers['Cache-Control'] = 'max-age=2629800, public, stale-while-revalidate=2592000'
  return response

@proxy_app.route('/dlsite/user/<id>')
def dlsite(id):
  data = requests.get('https://www.dlsite.com/eng/circle/profile/=/maker_id/' + id).text
  soup = BeautifulSoup(data, 'html.parser')
  response = make_response(jsonify({
    "name": soup.find('strong', class_='prof_maker_name').string
  }), 200)
  response.headers['Cache-Control'] = 'max-age=2629800, public, stale-while-revalidate=2592000'
  return response