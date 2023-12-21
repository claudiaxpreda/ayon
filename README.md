# Ayon - Daily Planner Application

## Description 
This is a planning application which offers the following functuonalities: 
- Create an account (User).
- Create Events/ Activities and ToDo lists.
- Receive reminders via Email for Events.

The application is split in services using Docker. 
The server part of the application is implemented in NodeJS. 
The client is an interactive CLI prompt implemented in Python. 
The reminder service is implemented in NodeJS.



## How to test the application

host = IP address of the testing machine, for Dockert Toolbox
        /localhost (linux | docker for windows)
        / 0.0.0.0 (other cases)
port = the port on which the container is mapped
port = 80

Examples of requests to test the functionality:

    0.  docker-compose up -d 

    1.  Register a user:
        POST  http://host:port/api/users/register 
        {
            "username" : "test",
            "password" : "test"
        }

    2.  Authenticate an user:
        POST http://host:port/api/users/login
        {
            "username" : "test",
            "password" : "test"
        }

    3.  Add an event for an user:
        POST http://host:port/users/events 
        {
            "title" : "My first event",
            "description" : "My firts event description",
            "location" : "Bucharest"
        }

    4.  See events added for an user:
        GET http://host:port/api/users/events

    5.  Update an event:
        PUT http://host:port/users/events/event_id 
        {
            "title" : "My first event",
            "description" : "My firts event description",
            "location" : "Bucharest"
        }, unde event_id este selectat din lista afisata la punctul 4;

    6. Repeaat 4 to observer the change.

    7. Delete an event:
        DELETE http://host:port/users/events/event_id, 
        -- where event_id is selected from the list dispalayed at 4.

    8. Repeaat 4 to observer the change.


  
