from db.store import AbstractStore
from app.main.message import Message, MessageStoreError
from db import get_db, query_db, del_query_db


class MessageStore(AbstractStore):
    """
    The message store responsible for the CRUD functions.
    """
    def store(self, message: Message):
        """
        Create a message entry.

        :param Message message:
        :rtype: dict
        :return: A message dict
        """
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
        """
        Read from the db.

        :param str query: query ready for execution.
        :rtype: dict
        :return: A message dict
        """
        stored_objects = query_db(query)
        messages = []
        for obj in stored_objects:
            messages.append(Message.from_tuple(obj).to_json())
        return messages

    def update(self, message_json):
        """
        Update a message in message table, automatically updated the unread
        field to 1.

        :param message_json: Message to update.
        """
        message_in_db = self.load_by_id(message_json['uid'])[0]
        if message_in_db:
            query = """UPDATE message SET sender="{0}", receiver="{1}", 
            message="{2}", subject="{3}", unread={4}  WHERE id={5}""".format(
                message_json['sender'],
                message_json['receiver'],
                message_json['message'],
                message_json['subject'],
                1,
                message_in_db['uid']
            )

            db = get_db()
            db.execute(query)
            db.commit()

    def delete(self, message_id):
        """
        Delete a specific message by ID, and return the deleted message.

        :param message_id: The message ID to delete
        :rtype: dict
        :return: A dict containing the message that hav been deleted.
        """
        message = self.load_by_id(message_id)
        if not message:
            raise MessageStoreError(MessageStoreError.NOT_FOUND)
        del_query_db('DELETE FROM message WHERE id == {0}'.format(message_id))
        return message[0]

    def load_by_id(self, message_id):
        """
        Composing an query to get an message with a specific message ID

        :param str message_id: The message ID
        :rtype; list
        :return: list of messages
        """
        query = 'SELECT * FROM message WHERE id == {0}'.format(message_id)
        return self.load(query)

    def load_by_receiver(self, receiver, unread=False):
        """
        Composing an query to get an message with a specific receiver.
        if unread is True, return only the unread messages.

        :param str receiver: The message receiver
        :param bool unread: Flag indicate unread messages.
        :rtype; list
        :return: list of messages with a specific receiver.
        """
        query = 'SELECT * FROM message WHERE receiver == "{0}"'.format(
            receiver)
        messages = self.load(query)
        if unread:
            messages = [
                message for message in messages if not message.get('unread')
            ]
        for message in messages:
            self.update(message)
        return messages
