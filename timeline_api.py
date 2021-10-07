import hug
import sqlite3
import sqlite_utils
from sqlite_utils import Database
import requests
import datetime
import json


db = Database(sqlite3.connect("timelines.db"))

def authenticate_user(username, password):
    """Authenticates a user"""
    print('auth called')
    r = requests.get("http://localhost:8000/users/"+username)
    user = json.loads(r.text)
    user = user["users"][0]
    if user["password"] == password:
        print('auth passed')
        return user
    print('auth failed')
    return False

@hug.get("/public_timeline/")
def public_timeline():
    return {"posts": db["posts"].rows_where(order_by = "timestamp desc")}

@hug.get("/user_timeline/{username}")
def user_timeline(response, username: hug.types.text):
    posts = []
    try:
        for row in db["posts"].rows_where("username = ?", [username], order_by = "timestamp desc"):
            posts.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": posts}

@hug.get("/home_timeline/{username}", requires=authenticate_user)
def home_timeline(response, username: hug.types.text):
    #TODO
    posts = []
    try:
        for row in db["posts"].rows_where("username = ? ORDER BY timestamp DESC", [username]):
            posts.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": posts}

@hug.get("/posts/{id}")
def retrieve_post(response, id: hug.types.number):
    posts = []
    try:
        post = db["posts"].get(id)
        posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": posts}

@hug.post("/posts/", status=hug.falcon.HTTP_201, requires=hug.authentication.basic(authenticate_user('stan98', 'p@ssw0rd')))
def create_post(
    username: hug.types.text,
    text: hug.types.text,
    repost: hug.types.text,
    response,
    user: hug.directives.user,
):
    posts = db["posts"]

    post = {
        "username": username,
        "text": text,
        "timestamp": datetime.datetime.now(),
        "repost": repost,
    }

    try:
        posts.insert(post)
        post["id"] = posts.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/posts/{post['id']}")
    return post
