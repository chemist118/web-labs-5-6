from werkzeug.security import check_password_hash


def check_user_password(user, password):
    return check_password_hash(user.password, password)


def validate_login(login):
    flag = False
    for c in login:
        flag = (c.isalpha() or c.isdigit()) is True
    return login.strip() != '' and flag


def validate_password(password):
    stop_chars = set(' ')
    return password.strip() != '' and not any((c in stop_chars) for c in password)
