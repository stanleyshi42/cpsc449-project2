import hug
import sqlite3
import sqlite_utils
from sqlite_utils import Database
import requests
import datetime


db = Database(sqlite3.connect("./var/posts.db"))

def authenticate_user(username, password):
    """Authenticates a user"""
    r = requests.get("http://localhost:8000/users/" + username)
    user = r.json()
    user = user["users"][0]     # Gets the user we want to auth

    if user["password"] == password:
        return user
    return False

@hug.get("/public_timeline/")
def public_timeline():
    """GET the Public Timeline; sorted by timestamp"""
    # Return in JSON format
    return {"posts": db["posts"].rows_where(order_by = "timestamp desc")}

@hug.get("/user_timeline/{username}")
def user_timeline(response, username: hug.types.text):
    """GET a user's User Timeline; sorted by timestamp"""
    posts = []
    try:
        for row in db["posts"].rows_where("username = ?", [username], order_by = "timestamp desc"):
            posts.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": posts}

@hug.get("/home_timeline/", requires=hug.authentication.basic(authenticate_user))
def home_timeline(
    response,
    user: hug.directives.user,
):
    """GET a user's Home Timeline; sorted by timestamp"""
    posts = []
    username = user["username"]

    # GET all the users the user is following
    r = requests.get("http://localhost:8000/users/" + username + "/following")
    r = r.json()
    following_list = []
    for row in r["users"]:
        following_list.append(row["following_id"])

    # Query all posts from users being followed
    try:
        for following_id in following_list:
            for row in db["posts"].rows_where("username = ?", [following_id]):
                posts.append(row)
        posts.sort(key=lambda post: post["timestamp"], reverse=True)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": posts}

@hug.get("/posts/{id}")
def retrieve_post(response, id: hug.types.number):
    """GET a post by its ID"""
    posts = []
    try:
        post = db["posts"].get(id)
        posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": posts}

@hug.post("/posts/", status=hug.falcon.HTTP_201, requires=hug.authentication.basic(authenticate_user))
def create_post(
    user: hug.directives.user,
    text: hug.types.text,
    repost: hug.types.text,
    response,
):
    """POST a user's post"""
    posts = db["posts"]

    post = {
        "username": user["username"],
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
