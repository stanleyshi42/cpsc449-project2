# CPSC 449 Project 2 - RESTful Microservices
In this project, we've built 2 RESTful back-end services for a mock microblogging service.

## Team Members
- Stanley Shi

## Setup
Install project requirements:
```bash
sudo apt update
sudo apt install --yes python3-pip ruby-foreman httpie sqlite3
python3 -m pip install hug sqlite-utils
sudo apt install --yes haproxy gunicorn
```

Navigate to the project directory:
```bash
cd cpsc449-project2
```

Configure HAProxy by copying /haproxy.cfg to /etc/haproxy/haproxy.cfg. Then, restart HAProxy:
```bash
sudo systemctl restart haproxy
```

Create databases:
```bash
./bin/init.sh
```

## Running the Project
Start both microservices:
```bash
foreman start
```

Open a new terminal.
Now, we can make calls to the project's API:
```bash
http GET localhost:80/public_timeline
```
```bash
http GET localhost:80/users
```

## User Authentication
Some of the API endpoints, like /home_timeline/, require user authentication. To enter user authentication information with HTTPie, use the -a flag:
```bash
http -a username:password GET localhost:80/home_timeline
```
For example:
```bash
http -a stan98:asdf GET localhost:80/home_timeline
```

## Multiple Instances and Load Balancing
This project is configured to perform load balancing between 3 instances of the timeline service.
We can run multiple instances of each service by using foreman's --formation, or -m, switch. Run the following to run 1 instance of the user service and 3 instances of the timeline service:
```bash
foreman start -m "user_api=1, timeline_api=3"
```

## Files
* Procfile
* timeline_api.py
* user_api.py
* README.md
* bin/init.sh
  * Script for creating the project's databases
* share/following.csv
* share/posts.csv
* share/users.csv
* share/haproxy-config
  * Contains additional configuration for HAProxy's config file
  * Used to add load balancing to the project
* var/
  * An empty directory that will hold our databases
  
## API Endpoints
### Timeline Service
* GET /public_timeline/
  * Returns Public Timeline
* GET /user_timeline/{username}
  * Returns the User Timeline of a specific user
* GET /home_timeline/
  * Requires user auth
  * Returns the Home Timeline of a specific, authenticated user
* GET /posts/{id}
  * Return a specific post by ID
* POST /posts/
  * Requires user auth
  * Creates a post

### User Service
* GET /users/
  * Returns all users
* GET /users/{username}
  * Returns a specific user by username
* POST /users/
  * Creates a new user
* GET /users/{username}/following/
  * Gets a user's following list
* POST /users/{username}/following/
  * Adds a new user to a specific user's following list

