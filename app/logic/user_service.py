from db import query_db


def query_user(user_name):
    """
    Create a query for a specific use name in users table.

    :param str user_name: The user name
    :rtype; bool
    :return: True if the user exists, false otherwise.
    """
    query = 'SELECT * FROM users WHERE user_name == "{0}"'.format(user_name)
    query = query_db(query)
    if query:
        return True
    return False


def validate_users(json_dict):
    """
    Validate user existence from the provided message in the db.

    :param dict json_dict: Message dict.
    :rtype; bool
    :return: True if the user exists, false otherwise.
    """
    sender_name = json_dict.get('sender', '')
    receiver_name = json_dict.get('receiver', '')
    if sender_name and receiver_name:
        return query_user(sender_name) and query_user(receiver_name)
    return False
