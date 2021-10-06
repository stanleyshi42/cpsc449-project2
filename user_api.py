import hug
import sqlite3
import sqlite_utils
from sqlite_utils import Database
import datetime

@hug.get("/users/")
def retrieve_users():
    return {"users": db["users"].rows}

db = Database(sqlite3.connect("mockroblog.db"))