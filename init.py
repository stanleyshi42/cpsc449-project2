import sqlite_utils
import datetime


def create_users_database():
    """Create and insert data into users database"""
    # Create/Recreate database
    db = sqlite_utils.Database("users.db", recreate=True)

    # Create and populate users table
    users = db["users"]
    users.insert({
        "username": "stan98",
        "bio": "hello there!",
        "email": "stan@email.com",
        "password": "asdf",
    }, pk="username")

    users.insert({
        "username": "john_johnson",
        "bio": ":)",
        "email": "john@gmail.com",
        "password": "password",
    })

    users.insert({
        "username": "jack_jackson",
        "bio": ":(",
        "email": "jack@yahoo.com",
        "password": "qwerty",
    })

    # Create and populate following table
    following = db["following"]
    following.insert({
        "id": 0,
        "follower_id": "stan98",
        "following_id": "john_johnson",
    }, pk="id", foreign_keys=[("follower_id", "users", "username"), ("following_id", "users", "username")])

    following.insert({
        "id": 1,
        "follower_id": "stan98",
        "following_id": "jack_jackson",
    })

    following.insert({
        "id": 2,
        "follower_id": "john_johnson",
        "following_id": "stan98",
    })

    following.insert({
        "id": 3,
        "follower_id": "john_johnson",
        "following_id": "jack_jackson",
    })

    following.insert({
        "id": 4,
        "follower_id": "jack_jackson",
        "following_id": "stan98",
    })

def create_timelines_database():
    # Create/Recreate database
    db = sqlite_utils.Database("timelines.db", recreate=True)

    posts = db["posts"]
    posts.insert({
        "id": 0,
        "username": "stan98",
        "text": "Hello world!",
        "timestamp": "2012-9-06T16:12:15",
        "repost": False,
    }, pk = "id")

    posts.insert({
        "id": 1,
        "username": "stan98",
        "text": "thank god it's friday",
        "timestamp": "2021-10-01T12:16:17",
        "repost": False,
    })

    posts.insert({
        "id": 2,
        "username": "jack_jackson",
        "text": "is this thing working",
        "timestamp": datetime.datetime.now(),
        "repost": False,
    })

    posts.insert({
        "id": 3,
        "username": "john_johnson",
        "text": "i h8 mondays",
        "timestamp": "2019-9-06T07:12:10",
        "repost": False,
    })

    posts.insert({
        "id": 4,
        "username": "stan98",
        "text": "covfefe",
        "timestamp": "2018-9-06T15:16:38",
        "repost": False,
    })

    posts.insert({
        "id": 5,
        "username": "jack_jackson",
        "text": "need coffee",
        "timestamp": "2018-9-06T06:16:59",
        "repost": False,
    })

create_users_database()
create_timelines_database()
