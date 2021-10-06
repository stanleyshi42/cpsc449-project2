import hug
import sqlite3
import sqlite_utils
from sqlite_utils import Database
import datetime


def create_database():
    # Create/Recreate database
    db = sqlite_utils.Database("mockroblog.db", recreate=True)

    # Create and populate users table
    users = db["users"]
    users.insert({
        "username": "stan98",
        "bio": "hello there!",
        "email": "stan@email.com",
        "password": "p@ssw0rd",
        "following": ["john_johnson", "jack_jackson"],
        "posts": [0, 1]
    }, pk="username")

    users.insert({
        "username": "john_johnson",
        "bio": ":)",
        "email": "john@email.com",
        "password": "abcdefg",
        "following": ["stan98"],
        "posts": []
    }, pk="username")

    users.insert({
        "username": "jack_jackson",
        "bio": ":(!",
        "email": "jack@yahoo.com",
        "password": "qwerty",
        "following": ["john_johnson"],
        "posts": [2]
    }, pk = "username")

    posts = db["posts"]
    posts.insert({
        "username": "stan98",
        "text": "Hello world!",
        "timestamp": datetime.datetime.now(),
        "repost": False,
        "id": 0
    }, pk = "id")

    posts.insert({
        "username": "stan98",
        "text": "thank god it's friday",
        "timestamp": datetime.datetime.now(),
        "repost": False,
        "id": 1
    }, pk = "id")

    posts.insert({
        "username": "jack_jackson",
        "text": "asdf",
        "timestamp": datetime.datetime.now(),
        "repost": False,
        "id": 2
    }, pk = "id")

# Create and connect to database
create_database()
db = Database(sqlite3.connect("mockroblog.db"))