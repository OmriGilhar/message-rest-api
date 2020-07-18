import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify, make_response)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, UserEntry


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    account_json = request.get_json()
    username = account_json.get('username', None)
    password = account_json.get('password', None)
    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif db.execute(
        'SELECT user_id FROM users WHERE user_name = ?', (username,)
    ).fetchone() is not None:
        error = 'User {} is already registered.'.format(username)

    if error is None:
        db.execute(
            'INSERT INTO users (user_name, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
        return make_response(jsonify('Account has been registered.'), 200)

    return make_response(jsonify('This account is already registered.'), 400)


@bp.route('/login', methods=['POST'])
def login():
    account_json = request.get_json()
    username = account_json.get('username', None)
    password = account_json.get('password', None)
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM users WHERE user_name = ?', (username,)
    ).fetchone()
    user = UserEntry(*user)

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user.password, password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user.user_id
        session['user_name'] = user.user_name
        return make_response(jsonify('login success.'), 200)
    return make_response(jsonify(error), 400)
