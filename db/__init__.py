import os
import sqlite3
from flask import g, current_app
from collections import namedtuple
import logging

UserEntry = namedtuple('UserEntry', 'user_id,user_name,password')


def init_db():
    db = get_db()
    try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'db.sql')) as f:
            sql = f.read()  # watch out for built-in `str`
            db.executescript(sql)
    except sqlite3.OperationalError as oe:
        logging.error("Could not found .sql schema, create db with "
                      "predefined sql schema\nError trace : {0}".format(
                       str(oe)))
        db.execute("""CREATE TABLE users( user_id INTEGER PRIMARY KEY,  
        user_name text, password text); CREATE TABLE message( id INTEGER 
        PRIMARY KEY, sender text, receiver text, message text, subject 
        text, date date, unread INTEGER);""")
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
