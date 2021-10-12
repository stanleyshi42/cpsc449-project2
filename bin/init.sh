#!/bin/sh

sqlite-utils insert ./var/users.db users --csv ./share/users.csv --detect-types --pk=username
sqlite-utils create-index ./var/users.db users username --unique bio email password

sqlite-utils insert ./var/users.db following --csv ./share/following.csv --detect-types --pk=id
sqlite-utils create-index ./var/users.db following id --unique follower_id following_id

sqlite-utils insert ./var/posts.db posts --csv ./share/posts.csv --detect-types --pk=id
sqlite-utils create-index ./var/posts.db posts id --unique username text timestamp repost
