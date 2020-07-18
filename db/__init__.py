import sqlite3
from flask import g, current_app


def init_db():
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
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
    return g.db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def del_query_db(query, args=()):
    get_db().execute(query, args)
    get_db().commit()
