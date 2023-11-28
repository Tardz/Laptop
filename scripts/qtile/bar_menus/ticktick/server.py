from flask import Flask, request, jsonify, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = 'awdnwudop8hoiwn1iuhe027887ocjnkl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

client_id = 'J7jnDtoFyf501eepIw'
client_secret = 'J8c@FHmETp9(MBh#_)c46j9#_Ike1cDP'
authorization_base_url = 'https://ticktick.com/oauth/authorize'
token_url = 'https://ticktick.com/oauth/token'
redirect_uri = 'https://0d39-155-4-149-181.ngrok-free.app/callback'
scope = ['tasks:read', 'tasks:write']

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

@app.route('/')
def home():
    return 'Hello, this is your local server!'

@app.route('/login')
def login():
    ticktick = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = ticktick.authorization_url(authorization_base_url)
    
    print(cache.get('oauth_state'))
    
    if not cache.get('oauth_state'):
        cache.set('oauth_state', state)
        return redirect(authorization_url)
    else:
        return "Already verified!"

@app.route('/callback')
def callback():
    state = cache.get('oauth_state')

    if request.args.get('state') != state:
        return f'Invalid state. Please try again. {request.args.get("state")}, {state}'

    ticktick = OAuth2Session(client_id, redirect_uri=redirect_uri)
    token = ticktick.fetch_token(
        token_url, 
        authorization_response=request.url, 
        client_secret=client_secret
    )

    print(token)

    cache.set('oauth_token', token)

    return 'Authorization successful!'

@app.route('/tasks')
def get_tasks():
    token = cache.get('oauth_token')
    
    if not token:
        return redirect(url_for('login'))

    ticktick = OAuth2Session(client_id, token=token)
    
    try:
        # Make a request to TickTick API to get tasks
        response = ticktick.get('https://api.ticktick.com/open/v1/project')
        response.raise_for_status()
        tasks = response.json()
        print(jsonify(tasks))
        return jsonify(tasks)
    except HTTPError as e:
        return f'Error accessing TickTick API: {e.response.text}', 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(host='0.0.0.0', port=5000)
