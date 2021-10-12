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

Create databases:
```bash
./bin/init.sh
```

## Running the Project
Start both microservices:
```bash
foreman start
```

Now, we can make calls to the project's API:
```bash
http GET localhost:80/public_timeline
```
```bash
http GET localhost:80/users
```

## Starting Multiple Instances
We can run multiple instances of each service by using the foreman --formation, or -m, switch. 

Run the following to run 1 instance of the user service and 3 instances of the timeline service:
```bash
foreman start -m "user_api=1, timeline_api=3"
```

## Load Balancing
We can configure HAProxy to perform load balancing between the 3 instances of the timeline service. To do this, append the contents of share/haproxy-config to the end of HAProxy's config file. To edit HAProxy's config file, use:
```bash
sudo nano /etc/haproxy/haproxy.cfg
```

## Files
* Procfile
* timeline_api.py
* user_api.py
* readme.md
* bin/init.sh
* share/following.csv
* share/posts.csv
* share/users.csv
* var/
  * An empty directory that will hold our databases
