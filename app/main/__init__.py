from flask import Flask
from logging.config import dictConfig


def create_app(app_name):
    create_log()
    app = Flask(app_name)
    app.logger.info("App stated successfully.")
    from . import auth
    app.register_blueprint(auth.bp)

    return app


def create_log():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })