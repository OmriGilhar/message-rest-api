# import pytest
# from db import init_db
# import tempfile
# from app.main.main import app
# import os
#
#
# @pytest.fixture(scope='function')
# def client():
#     db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     app.config['TESTING'] = True
#
#     with app.test_client() as client:
#         with app.app_context():
#             init_db()
#         yield client
#
#     os.close(db_fd)
#     os.unlink(app.config['DATABASE'])
#
#
# @pytest.mark.parametrize('json_dict,expected', [
#     (
#             {
#                 "sender": "Dummy Sender",
#                 "receiver": "Dummy Receiver",
#                 "message": "This is a test message",
#                 "subject": "Test Message"
#             },
#             {
#                 "message": "This is a test message",
#                 "receiver": "Dummy Receiver",
#                 "sender": "Dummy Sender",
#                 "subject": "Test Message",
#                 "unread": 0
#             }
#     )
# ])