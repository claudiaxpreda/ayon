# Ayon - Daily Planner Application

## Etapa 2 - testing

Etapa doi a constat in implementarea autentificarii unui user si implemenntarea operatiilor
cu evenimente.

host = adresa ip a masinii docker, in cazul Dockert Toolbox
        /localhost (pentru linux sau docker for windows)
        / 0.0.0.0 (in anumite cazuri)
port = portul pe care este mapat containerul
port = 80

Acestea se pot testa astfel, urmand in ordine urmatoarele requesturi:

    0.  docker-compose up -d 

    1.  Inregistrarea unui user:
        POST  http://host:port/api/users/register 
        {
            "username" : "test",
            "password" : "test"
        }

    2.  Autentificarea unui user:
        POST http://host:port/api/users/login
        {
            "username" : "test",
            "password" : "test"
        }

    3.  Adaugarea unui eveniment pentru un user:
        POST http://host:port/users/events 
        {
            "title" : "My first event",
            "description" : "My firts event description",
            "location" : "Bucharest"
        }

    4.  Vizualizarea evenimentelor adaugate de userul curent:
        GET http://host:port/api/users/events

    5.  Modificarea unui eveniment 
        PUT http://host:port/users/events/event_id 
        {
            "title" : "My first event",
            "description" : "My firts event description",
            "location" : "Bucharest"
        }, unde event_id este selectat din lista afisata la punctul 4;

    6. Repetarea punctului 4 pentru a observa modificarea

    7. Stergerea unui eveniment:
        DELETE http://host:port/users/events/event_id, 
        -- unde event_id este selectat din lista afisata la punctul 4;

    8. Repetarea punctului pentru a observa efectul 


  