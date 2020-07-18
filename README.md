
  
#  Message REST API  
  
[![Flask](https://i.ibb.co/s5srDW5/flask-icon-small.png)](https://flask.palletsprojects.com/en/1.1.x/)[![python](https://i.ibb.co/6ny3KTv/python-icon.png)](https://www.python.org/)  
  
This is a Flask based API.  
writen in:  
 - Python 3.8  
---  
### Prerequisites  
Please make sure you have the following interpreter on your machine:  
[Python 3.8](https://www.python.org/downloads/)  
  
---  
## Getting Started  
  
So you want to start play with the code, you got it!  
Clone the repository to your machine,  
Open python interpreter, rediract to the project folder and run:  
```  
pip install -r requirements.txt  
```  
You can use virtual environment (see [here](https://docs.python.org/3/tutorial/venv.html))  
make sure you run the right interpreter, and run the main.py script  
```  
python app/main/main.py  
```  
And the server is up and running!  
  
---  
## Server URLs  
You can reach the following URLs:  
  
| URL                                          | Method | Accepts  | Return |       `{Variable}`      |         Description          |  
| :------------------------------------------- |:------:| :-------:| :----: | :---------------------: | :--------------------------: |  
| /auth/register                              | POST   |   JSON   |  JSON  |        -                | Register a user  |  
| /auth/login                                 | POST   |   JSON   |  JSON  |        -                |       Login a user     |  
| /messages/new                             | POST   |   JSON   |  JSON  |        -                |   Create a new Message|  
| /messages?`{unread}`                       | GET    |    -     |  JSON  |  Optional - unread messages   |Get all message by logged-in user|  
| /message/`{message_id}`                  | GET    |    -     |  JSON  | Message ID  |   Return a message by ID  |  
| /message/`{message_id}`                        | DELETE |    -     |  JSON  |     Message ID      |      Delete and Return a message by ID     |  
  
---  
  
## Running the tests  
  
From the root of the repository, activate the virtualenv, and run the tests:

```  
pytest -vvv
```
-vvv for verbose   
  
---  
  
## Author  
  
* **Omri Gilhar** - [Github Profile](https://github.com/OmriGilhar)  
  
## License