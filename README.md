# UE-AD-A1-MIXTE

## Structure of the project

The project contains 4 microservices as shown below :

![services.png](assets%2Fservices.png)

The goal of this project is to understand how different APIs (REST, graphQL, gRPC) can communicate 
and to create a simple application where users can book to see a movie.

Each service stores data in a JSON file.

### User Service

Located in the /user folder. This service manages the users (create, read, update and delete). All the routes
are accessible via HTTP because it is a REST Api. This service is the entreypoint to the whole system 
and interacts with the other services using different methods (graphQL, gRPC...). 

### Movie Service

Located in the /movie folder. This service gives CRUD functionalities regarding Movies as a graphQL API. 

### Booking Service

Located in the /booking folder. This service is used to manage the bookings to the movies each user want to see.  
Since it is a gRPC server, other services need to open a channel and have the same protos files in order to communicate with it.
### Times Service

Located in the /showtime folder. Contains all the informations and CRUD functionnalities about 
showtimes for the movies. Just like the Booking Service, the Times Service is a gRPC server. 

## How to deploy

First, clone this repository on your machine. 

Then, run :

```
docker-compose up
```

If you need to delete the containers :
```
docker-compose rm
```

And finally to rebuild the image if needed :
```
docker-compose up --build
```

## Access the different services

The services are inside their own container. Since all containers are in the same network, they can communicate together.

The services are also forwarded on the host machine (localhost) with the following ports :

- User : 8080
- Movie : 5003
- Booking : 5002
- Showtime : 5001

These ports are set in the .env file. When starting the containers, the environment variables are loaded and fetched in the python files. 

Postman Collections are available in the folder /postman. 
Be aware, only HTTP requests are available since gRPC/graphQL cannot be exported from Postman :(