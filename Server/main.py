# coding=utf-8
import sys
from importlib import reload

from flask import Flask, request, session, json, jsonify
from flask_cors import CORS, cross_origin

# Создаём приложение
from dao import userDao, tasksDAO
from dao.checking import userChecking, taskChecking
from entities.models import Task
from storage.database import init_db, db_session

app = Flask(__name__)
CORS(app)

# Конфигурируем
# Устанавливаем ключ, необходимый для шифрования куки сессии
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/api/login', methods=['GET'])
@cross_origin()
def set_login():
    login = request.args.get('user_login')
    password = request.args.get('user_password')
    error = None

    code = 422
    if not login:
        error = "Login required"
    elif not password or login.strip() == '':
        error = "Password required"

    user = None
    if error is None and login and password:
        user = userDao.get_user_by_login(login)
        if not user:
            error = "User does not exist"
        elif not userChecking.check_user_password(user, password):
            error = "Invalid password"

    if error is None:
        session['user_id'] = user.id
        code = 200
        return jsonify(json.dumps(user.serialize())), code

    return jsonify(error=error), code


@app.route('/registration', methods=['POST'])
@cross_origin()
def add_registration():
    json_request = request.get_json()
    login = json_request['login']
    password = json_request['password1']
    password2 = json_request['password2']

    error = None
    code = 422
    if not login:
        error = "Login required"
    elif not userChecking.validate_login(login):
        error = "Login is empty or contains not only numbers and letters"
    elif not password:
        error = "Password required"
    elif not userChecking.validate_password(password):
        error = "Password is empty or contains a forbidden space character"
    elif not password2:
        error = "Password confirmation required"
    elif password != password2:
        error = "Passwords do not match"

    user = None
    if error is None and login and password and password2:
        user = userDao.get_user_by_login(login)
    if user:
        error = "Login already exists"

    if error is None:
        userDao.add_user(login, password)
        user = userDao.get_user_by_login(login)
        session['user_id'] = user.id
        code = 200
        return jsonify(json.dumps(user.serialize())), code

    return jsonify(error=error), code


@app.route('/api/todos', methods=['GET'])
@cross_origin()
def get_todos():
    user_id = int(request.args.get('user_id'))
    if user_id != session['user_id']:
        return jsonify(error='Access denied'), 403
    json_todos = json.dumps(Task.serialize_list(tasksDAO.get_tasks_by_user_id(user_id)))

    return jsonify(json_todos), 200


@app.route('/api/todos', methods=['POST'])
def add_task():
    json_request = request.get_json()
    user_id = int(json_request['user_id'])

    if user_id != session['user_id']:
        return jsonify(error='Access denied'), 403

    error = None
    code = 422
    title = json_request['title']
    description = json_request['description']
    completed = json_request['completed']

    if not title:
        error = "Required task title"
    elif not taskChecking.validate_task_title(title):
        error = "Task title is empty"
    elif tasksDAO.get_task_by_title('', title, user_id):
        error = "This title already exists"

    if error is None:
        todo = tasksDAO.add_task(user_id, title, description, completed)
        code = 200
        return jsonify(json.dumps(todo.serialize())), code
    return jsonify(error=error), code


@app.route('/api/todos/<todo_id>', methods=['POST'])
def task_update(todo_id):
    json_request = request.get_json()
    user_id = int(json_request['user_id'])
    if user_id != session['user_id']:
        return jsonify(error='Access denied'), 403

    error = None
    code = 422
    title = json_request['title']
    description = json_request['description']
    completed = json_request['completed']
    task = tasksDAO.get_task_by_id(todo_id)
    if task is None:
        return jsonify(error="There is no such task"), 404
    current_title = task.title

    if not title:
        error = "Required task title"
    elif not taskChecking.validate_task_title(title):
        error = "Task title is empty"
    elif tasksDAO.get_task_by_title(current_title, title, user_id):
        error = "This title already exists"

    if error is None:
        todo = tasksDAO.update_task(user_id, todo_id, title, description, completed)
        code = 200
        return jsonify(json.dumps(todo.serialize())), code
    return jsonify(error=error), code


@app.route('/api/todos/delete', methods=['POST'])
@cross_origin()
def task_remove():
    json_request = request.get_json()
    user_id = int(json_request['user_id'])
    if user_id != session['user_id']:
        return jsonify(error='Access denied'), 403

    todo_id = json_request['id']

    error = None
    code = tasksDAO.remove_task(user_id, todo_id)
    if code == 404:
        error = 'There is no such task'
    return jsonify(error=error), code


@app.route('/api/logout', methods=['POST'])
@cross_origin()
def logout():
    json_request = request.get_json()
    user_id = int(json_request['user_id'])
    if user_id != session['user_id']:
        return jsonify(error='Access denied'), 403

    session['user_id'] = None
    return jsonify(error=None), 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    reload(sys)
    init_db()
    app.run('localhost', 5000)
