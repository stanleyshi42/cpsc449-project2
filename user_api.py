import hug
import sqlite3
import sqlite_utils
from sqlite_utils import Database
import datetime

@hug.get("/users/")
def retrieve_users():
    return {"users": db["users"].rows}

@hug.get("/users/{username}")
def retrieve_user(response, username: hug.types.text):
    users = []
    try:
        user = db["users"].get(username)
        users.append(user)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": users}

db = Database(sqlite3.connect("users.db"))