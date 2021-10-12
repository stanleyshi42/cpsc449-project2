import hug
import sqlite3
import sqlite_utils
from sqlite_utils import Database


db = Database(sqlite3.connect("./var/users.db"))

@hug.get("/users/")
def retrieve_users():
    """GET all users"""
    return {"users": db["users"].rows}

@hug.get("/users/{username}")
def retrieve_user(response, username: hug.types.text):
    """GET a user by their username"""
    users = []
    try:
        user = db["users"].get(username)
        users.append(user)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": users}

@hug.post("/users/", status=hug.falcon.HTTP_201)
def create_user(
    username: hug.types.text,
    bio: hug.types.text,
    email: hug.types.text,
    password: hug.types.text,
    response,
):
    """POST a new user"""
    users = db["users"]

    user = {
        "username": username,
        "bio": bio,
        "email": email,
        "password": password,
    }

    try:
        users.insert(user)
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/users/{user['username']}")
    return user

@hug.get("/users/{username}/following")
def retrieve_following(response, username: hug.types.text):
    """GET a user's following list"""
    users = []
    try:
        for row in db["following"].rows_where("follower_id = ?", [username]):
            users.append(row)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": users}

@hug.post("/users/{username}/following", status=hug.falcon.HTTP_201)
def create_following(
    username: hug.types.text,
    following_id: hug.types.text,
    response,
):
    """POST a new follower"""
    follower = {
        "follower_id": username,
        "following_id": following_id,
    }

    try:
        db["following"].insert(follower)
        follower["id"] = db["following"].last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/following/{follower['id']}")
    return follower
