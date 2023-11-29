from flask import Flask, request, jsonify, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
import time

import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = 'awdnwudop8hoiwn1iuhe027887ocjnkl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

client_id = 'J7jnDtoFyf501eepIw'
client_secret = 'J8c@FHmETp9(MBh#_)c46j9#_Ike1cDP'
authorization_base_url = 'https://ticktick.com/oauth/authorize'
token_url = 'https://ticktick.com/oauth/token'
base_url = 'https://api.ticktick.com/open/v1/'
redirect_uri = 'https://0d39-155-4-149-181.ngrok-free.app/callback'
scope = ['tasks:read', 'tasks:write']

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.Float, nullable=False)
    expires_in = db.Column(db.Float, nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column_id = db.Column(db.Float, nullable=True)
    content = db.Column(db.String(255), nullable=True)
    desc = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.String(255), nullable=True)
    task_id = db.Column(db.String(255), nullable=False)
    is_all_day = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Float, nullable=False)
    project_id = db.Column(db.Float, nullable=False)
    repeat_flag = db.Column(db.String(255), nullable=True)
    sort_order = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Float, nullable=False)
    time_zone = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    linked_to_project = db.relationship('Projects', backref='project', lazy=True)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(20), nullable=False)
    group_id = db.Column(db.String(255), nullable=False)
    item_id = db.Column(db.String(255), nullable=False)
    kind = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    sort_order = db.Column(db.Float, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))  # Adjust ForeignKey to reference task_dir.id

@app.route('/login')
def login():
    ticktick = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = ticktick.authorization_url(authorization_base_url)
    
    if not Token.query.first():
        cache.set('oauth_state', state)
        return redirect(authorization_url)
    else:
        return jsonify({"result": "oauth token active"})

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

    stored_token = Token(
        access_token=token['access_token'],
        expires_at=token['expires_at'],
        expires_in=token['expires_in']
    )
    
    db.session.add(stored_token)
    db.session.commit()

    return 'Authorization successful!'

@app.route('/projects')
def get_projects():
    token = Token.query.first()

    if not token or token.expires_at < time.time():
        return redirect(url_for('login'))
    
    token_dict = {
        'access_token': token.access_token,
        'expires_at': token.expires_at,
        'expires_in': token.expires_in
    }
    
    ticktick = OAuth2Session(client_id, token=token_dict)
    
    try:
        response = ticktick.get(f'{base_url}project')
        response.raise_for_status()
        tasks = response.json()
        return jsonify(tasks)
    
    except HTTPError as e:
        return f'Error accessing TickTick API: {e.response.text}', 500
    
@app.route('/project')
def get_project():
    token = Token.query.first()

    if not token or token.expires_at < time.time():
        return redirect(url_for('login'))
    
    token_dict = {
        'access_token': token.access_token,
        'expires_at': token.expires_at,
        'expires_in': token.expires_in
    }
    
    ticktick = OAuth2Session(client_id, token=token_dict)
    
    try:
        project_id = request.args.get("project_id")
        response = ticktick.get(f'{base_url}project/{project_id}/data')
        response.raise_for_status()
        tasks = response.json()
        return jsonify(tasks)
    
    except HTTPError as e:
        return f'Error accessing TickTick API: {e.response.text}', 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
