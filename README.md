# CPSC 449 Project 2 - RESTful Microservices
In this project, we've built 2 RESTful back-end services for a mock microblogging service.

## Team Members
- Stanley Shi

## Setup
Navigate to the project directory:
```bash
cd cpsc449-project2
```

Create the databases:
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
You can run multiple instances of each service by using the foreman --formation, or -m, switch.
Run the following to run 1 instance of the user service and 3 instances of the timeline service.

```bash
foreman start -m "user_api=1, timeline_api=3"
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
  * An empty directory that holds our databases
