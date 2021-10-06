import hug
import sqlite3
import sqlite_utils
from sqlite_utils import Database
import datetime


@hug.get("/posts/")
def posts():
    return {"posts": db["posts"].rows}

@hug.get("/posts/{id}")
def retrieve_post(response, id: hug.types.number):
    posts = []
    try:
        post = db["posts"].get(id)
        posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"posts": posts}

@hug.post("/posts/", status=hug.falcon.HTTP_201)
def create_post(
    username: hug.types.text,
    text: hug.types.text,
    repost: hug.types.text,
    response,
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