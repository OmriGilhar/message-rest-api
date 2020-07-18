from db.store import AbstractStore
from app.main.message import Message
from db import get_db, query_db, del_query_db


class MessageNotFound(Exception):
    pass


class MessageStore(AbstractStore):
    def store(self, message: Message):
        db = get_db()
        db.execute("INSERT INTO message ("
                   "id, sender, receiver, message, subject, date, unread"
                   ") VALUES (?,?,?,?,?,?,?)",
                   (message.id, message.sender, message.receiver,
                    message.message, message.subject, message.creation_date,
                    message.unread))
        db.commit()

        message = self.load_by_id(message.id)
        return message

    def load(self, query):
        stored_objects = query_db(query)
        messages = []
        for obj in stored_objects:
            messages.append(Message.from_tuple(obj).to_json())
        return messages

    def update(self, message_json):
        message_in_db = self.load_by_id(message_json['uid'])[0]
        if message_in_db:
            query = """UPDATE message SET sender="{0}", receiver="{1}", 
            message="{2}", subject="{3}", unread={4}  WHERE id={5}""".format(
                message_json['sender'],
                message_json['receiver'],
                message_json['message'],
                message_json['subject'],
                1,
                message_json['uid']
            )

            db = get_db()
            db.execute(query)
            db.commit()

    def delete(self, message_id):
        message = self.load_by_id(message_id)
        if not message:
            raise MessageNotFound("Message ID {0} was not found.".format(
                message_id))
        del_query_db('DELETE FROM message WHERE id == {0}'.format(message_id))
        return message

    def load_by_id(self, message_id):
        query = 'SELECT * FROM message WHERE id == {0}'.format(message_id)
        return self.load(query)

    def load_by_receiver(self, receiver, unread=False):
        query = 'SELECT * FROM message WHERE receiver == "{0}"'.format(receiver)
        messages = self.load(query)
        if not unread:
            for message in messages:
                self.update(message)
            return messages
        messages = [message for message in messages if not message.get(
            'unread')]
        for message in messages:
            self.update(message)
        return messages
