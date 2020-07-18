import sqlite3
from flask import g

DATABASE = ':memory:'


def init_db(app):
    with app.app_context():
        db = get_db()
        # with app.open_resource('schema.sql', mode='r') as f:
        #     db.cursor().executescript(f.read())
        try:
            db.execute('''CREATE TABLE message( id INTEGER PRIMARY KEY,
             sender text, receiver text, message text, subject text, 
             date date, unread INTEGER)''')
        except sqlite3.OperationalError as oe:
            # TODO: check for return code
            pass
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def del_query_db(query, args=()):
    get_db().execute(query, args)
    get_db().commit()
