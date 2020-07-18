from flask import Flask


def create_app(app_name):
    app = Flask(app_name)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
