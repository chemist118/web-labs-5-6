from sqlalchemy import func
from entities.models import Task
from storage.database import db_session


def get_tasks_count(q):
    count_q = q.statement.with_only_columns([func.count()])
    count = q.session.execute(count_q).scalar()
    return count


def add_task(user_id, title, description, status):
    db_session.add(Task(None, user_id, title, description, status))
    db_session.commit()
    return get_task_by_title('', title, user_id)


def get_tasks_by_status(user_id, task_status):
    return Task.query.filter(Task.status == task_status and Task.user_id == user_id).order_by(Task.id)


def get_tasks_by_user_id(user_id):
    return Task.query.filter(Task.user_id == user_id).order_by(Task.id)


def get_tasks_by_title(user_id, title):
    search = "%{}%".format(title)
    return Task.query.filter(Task.title.ilike(search)).filter(Task.user_id == user_id).order_by(Task.id)


def get_task_by_id(task_id):
    return Task.query.filter(Task.id == task_id).first()


def get_task_by_title(current_title, title, user_id):
    if current_title == '':
        return Task.query.filter(Task.title == title and Task.user_id == user_id).first()
    else:
        return Task.query.filter(Task.title != current_title)\
            .filter(Task.title == title and Task.user_id == user_id).first()


def remove_task(user_id, task_id):
    task = get_task_by_id(task_id)
    if task is None:
        return 404
    if task.user_id != user_id:
        return 403
    db_session.delete(task)
    db_session.commit()
    return 200


def update_task(user_id, task_id, title, description, completed):
    task = get_task_by_id(task_id)
    if task is None:
        return None
    if task.user_id != user_id:
        return task
    task.title = title
    task.description = description
    task.completed = completed
    db_session.commit()
    return task
