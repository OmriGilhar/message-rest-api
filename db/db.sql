CREATE TABLE users( user_id INTEGER PRIMARY KEY, user_name text, password text);
CREATE TABLE message( id INTEGER PRIMARY KEY, sender text, receiver text,
message text, subject text, date date, unread INTEGER);