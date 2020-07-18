from db import init_db
from flask import Flask, g, request
from app.logic import message_service as ms

app = Flask(__name__)


# Post Create message
@app.route('/messages/new', methods=['GET', 'POST'])
def write_message():
    if request.method == 'POST':
        json_dict = request.get_json()
        return ms.write_message(json_dict)


# Get all messages from a specific user
@app.route('/messages/<receiver>', methods=['GET', 'POST'])
def get_message(receiver):
    if request.method == 'GET':
        unread = request.args.get('unread')
        return ms.get_message_by_receiver(receiver, unread)


# get and delete
@app.route('/message/<message_id>', methods=['GET', 'DELETE'])
def get_or_delete_message_by_id(message_id):
    if request.method == 'GET':
        return ms.get_message_by_id(message_id)
    if request.method == 'DELETE':
        return ms.delete_message_by_id(message_id)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    init_db(app)
    app.run(threaded=True, port=5000)