from flask import Flask, request, jsonify, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from sqlalchemy import JSON
from flask_migrate import Migrate

import time

import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = 'awdnwudop8hoiwn1iuhe027887ocjnkl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

client_id = 'J7jnDtoFyf501eepIw'
client_secret = 'J8c@FHmETp9(MBh#_)c46j9#_Ike1cDP'
authorization_base_url = 'https://ticktick.com/oauth/authorize'
token_url = 'https://ticktick.com/oauth/token'
base_url = 'https://api.ticktick.com/open/v1/'
redirect_uri = 'http://127.0.0.1:5000/callback'
scope = ['tasks:read', 'tasks:write']

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.Float, nullable=False)
    expires_in = db.Column(db.Float, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255), nullable=True)
    project_id = db.Column(db.String(255), nullable=True)
    # sort_order = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(255), nullable=True)
    content = db.Column(db.String(255), nullable=True)
    desc = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.String(255), nullable=True)
    is_all_day = db.Column(db.Boolean, nullable=True)
    priority = db.Column(db.Integer, nullable=True)
    repeat_flag = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, nullable=True)
    column_id = db.Column(db.String(255), nullable=True)
    parent_id = db.Column(db.String(255), nullable=True)
    child_ids = db.Column(JSON, nullable=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    kind = db.Column(db.String(20), nullable=True)
    project_id = db.Column(db.String(255), nullable=False)
    group_id = db.Column(db.String(255), nullable=True)
    sort_order = db.Column(db.Integer, nullable=True)
    color = db.Column(db.String(20), nullable=True)

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
def get_stored_projects():
    projects = Project.query.order_by(Project.group_id).all()
    print("getting stored")
    projects_json = [{
            'name': project.name, 
            'kind': project.kind,
            'project_id': project.project_id, 
            'group_id': project.group_id,
            'sort_order': project.sort_order,
            'color': project.color
            } for project in projects]

    return jsonify(projects_json)
    
@app.route('/updated_projects')    
def get_updated_projects():
    token = Token.query.first()

    if not token or token.expires_at < time.time():
        return "", 302
    
    token_dict = {
        'access_token': token.access_token,
        'expires_at': token.expires_at,
        'expires_in': token.expires_in
    }
    
    ticktick = OAuth2Session(client_id, token=token_dict)
    
    try:
        response = ticktick.get(f'{base_url}project')
        response.raise_for_status()
        projects = response.json()

        for project in projects:
            already_exists = Project.query.filter_by(project_id=project.get("id")).first()

            if not already_exists:
                project_to_store = Project(
                    name = project.get("name"),
                    kind = project.get("kind"),
                    project_id = project.get("id"),
                    group_id = project.get("groupId"),
                    color = project.get("color"),
                    sort_order = int(project.get("sortOrder"))
                )
                db.session.add(project_to_store)
                
        db.session.commit()

        return redirect(url_for('get_stored_projects'))
    
    except HTTPError as e:
        return f'Error accessing TickTick API: {e.response.text}', 500
    
@app.route('/tasks')
def get_stored_tasks():
    project_id = request.args.get("project_id")

    tasks = Task.query.filter_by(project_id=project_id).all()

    def get_all_subtasks(parent_task, task_dict):
        """
        Recursively get all subtasks for a given parent task.
        """
        subtasks = []
        child_ids = parent_task.child_ids or []

        for child_id in child_ids:
            child_task = task_dict.get(child_id)
            if child_task:
                subtasks.append(child_task)
                subtasks.extend(get_all_subtasks(child_task, task_dict))

        return subtasks

    task_dict = {task.task_id: task for task in tasks}
    ordered_tasks = []

    for task in tasks:
        if not task.parent_id:
            ordered_tasks.append(task)
            subtasks = get_all_subtasks(task, task_dict)
            ordered_tasks.extend(subtasks)

    tasks_json = [{
            'task_id': task.task_id, 
            'project_id': task.project_id,
            'title': task.title,
            'content': task.content,
            'desc': task.desc, 
            'start_date': task.start_date,
            'due_date': task.due_date,
            'is_all_day': task.is_all_day,
            'priority': task.priority,
            'repeat_flag': task.repeat_flag,
            'status': task.status,
            'column_id': task.column_id,
            'parent_id': task.parent_id,
            'child_ids': task.child_ids 
            } for task in ordered_tasks]
    return jsonify(tasks_json)
    
@app.route('/updated_tasks')
def get_updated_tasks():
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

        for task in tasks["tasks"]:
            print(task, "\n\n")
            already_exists = Task.query.filter_by(task_id=task.get("id")).first()
            if not already_exists and task.get("id") != None:
                child_ids = None
                if task.get("childIds"):
                    child_ids = []
                    for child in task.get("childIds"):
                        child_ids.append(child)

                task_to_store = Task(
                    task_id = task.get("id"),
                    project_id = task.get("projectId"),
                    title = task.get("title"),
                    content = task.get("content"),
                    desc = task.get("desc"),
                    start_date = task.get("startDate"),
                    due_date = task.get("dueDate"),
                    is_all_day = task.get("isAllDay"),
                    priority = task.get("priority"),
                    repeat_flag = task.get("repeatFlag"),
                    status = task.get("status"),
                    column_id = task.get("columnId"),
                    parent_id = task.get("parentId"),
                    child_ids = child_ids
                )
                db.session.add(task_to_store)
                
        db.session.commit()
        return redirect(url_for('get_stored_tasks', project_id=project_id))
    
    except HTTPError as e:
        return f'Error accessing TickTick API: {e.response.text}', 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=True)
