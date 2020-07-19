from datetime import datetime
import logging
import uuid


class MessageStoreError(Exception):
    INVALID = 'One of the fields is invalid.'
    NOT_FOUND = 'Message not found.'
    NO_UNREAD_MESSAGES = 'No unread messages found.'
    NO_NEW_MESSAGES = 'There is no new messages.'

    def __init__(self, error):
        self.error = error
        super(self.__class__)


class Message:
    """
    This class representing a message.
    """
    def __init__(self, sender, receiver, message, subject, unread=0):
        """
        Class initiator.

        :param str sender: Sender name
        :param str receiver: receiver name
        :param str message: message name
        :param str subject: subject name
        :param int unread: unread flag
        """
        if not self.validate_inputs(sender, receiver, message, subject):
            raise MessageStoreError(MessageStoreError.INVALID)
        self.__uid = uuid.uuid4().int >> 96
        self.__sender = sender
        self.__receiver = receiver
        self.__message = message
        self.__subject = subject
        self.__creation_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.__unread = unread

    @staticmethod
    def validate_inputs(sender, receiver, message, subject):
        """
        validate message properties

        :param str sender: Sender name
        :param str receiver: Receiver name
        :param str message: Message content
        :param str subject: Message subject
        :rtype: bool
        :return: True if all properties are valid, False otherwise.
        """
        inputs_ok = True
        if not sender:
            logging.error("Empty sender is not allowed")
            inputs_ok = False
        if not receiver:
            logging.error("Empty receiver is not allowed")
            inputs_ok = False
        if not message:
            logging.error("Empty message is not allowed")
            inputs_ok = False
        if not subject:
            logging.error("Empty subject is not allowed")
            inputs_ok = False
        return inputs_ok

    @property
    def id(self):
        return self.__uid

    @property
    def sender(self):
        return self.__sender

    @property
    def receiver(self):
        return self.__receiver

    @property
    def message(self):
        return self.__message

    @property
    def subject(self):
        return self.__subject

    @property
    def creation_date(self):
        return self.__creation_date

    @property
    def unread(self):
        return self.__unread

    def to_json(self):
        """
        Return a dict representation of the message

        :rtype: dict
        """
        return {
            'uid': self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "message": self.message,
            "subject": self.subject,
            "creation_date": self.creation_date,
            'unread': self.unread
        }

    @classmethod
    def from_dict(cls, json_dict):
        """
        Alternate constructor converting dict into a Message obj

        :param json_dict: JSON dict containing message content.
        :rtype: Message
        :return: A message object representing the given JSON dict.
        """
        self = cls(**json_dict)
        return self

    @classmethod
    def from_tuple(cls, json_tuple):
        """
        Alternate constructor converting tuple into a Message obj

        :param tuple json_tuple: JSON tuple containing message content.
        :rtype: Message
        :return: A message object representing the given JSON dict.
        """
        message = cls(json_tuple[1], json_tuple[2], json_tuple[3],
                      json_tuple[4], json_tuple[6])
        message.__uid = json_tuple[0]
        return message
