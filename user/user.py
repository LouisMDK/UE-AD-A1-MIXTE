# REST API
import time

from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
import grpc
from concurrent import futures

# import booking_pb2
# import booking_pb2_grpc
# import movie_pb2
# import movie_pb2_grpc

# CALLING GraphQL requests
# todo to complete
from flask import Flask, render_template, request, jsonify, make_response
import requests
import time
import json

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
moviePort = 3200
bookingPort = 3201
showtime = 3202


def request_service(method, path):
    try:
        req = method(path, json=request.get_json())
        return make_response(jsonify(req.json()), req.status_code)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

def request_graphql(path, query):
    try:
        req = requests.post(path, json={'query': query})
        return make_response(jsonify(req.json()), req.status_code)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_all():
    return make_response(jsonify(users), 200)


@app.route("/users", methods=['POST'])
def create_user():
    req = request.get_json()
    if req["name"] is None:
        return make_response(jsonify({"error": "attribut name missing"}), 400)
    id = req["name"].lower().replace(" ", "_")
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify({"error": "user ID already exists"}), 409)
    name = req["name"].lower().title()
    lastActive = int(time.time())
    res = {
        "id": id,
        "name": name,
        "last_active": lastActive
    }
    users.append(res)
    return make_response(jsonify(res), 200)


@app.route("/users/<id>", methods=['GET'])
def get_user_byid(id):
    for user in users:
        if str(user["id"]) == str(id):
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "user ID don't exists"}), 400)


@app.route("/users/<id>", methods=['PUT'])
def create_update_user(id):
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(id):
            if "name" in req:
                user["name"] = req["name"]
            if "last_active" in req:
                user["last_active"] = req["last_active"]
            return make_response(jsonify(req), 200)
    req["id"] = id
    return create_user()


@app.route("/users/<id>", methods=['DELETE'])
def delete_user_by_id(id):
    for i, user in enumerate(users):
        if str(user["id"]) == str(id):
            tmpUser = user
            del users[i]
            return make_response(jsonify(tmpUser), 200)
    return make_response(jsonify({"error": "there is no user to delete for this id"}), 400)


# movie delegation


@app.route("/movies", methods=["GET"])
def get_all_movies():
    query = """
            query Movies {
                movies {
                    id
                    title
                    director
                    rating
                }
            }
            """

    return request_graphql(f"http://{HOST}:{moviePort}/graphql", query)


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    query = """
        query Movie_with_id {
            movie_with_id(_id: "%s") {
                id
                title
                director
                rating
            }
        }
        """ % movieid

    return request_graphql(f"http://{HOST}:{moviePort}/graphql", query)


@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    title = ""
    if request.args:
        title = request.args["title"]
    if not title:
        return make_response(jsonify({"error": "movie title not found"}), 400)
    query = """
        query Movie_with_title {
            movie_with_title(_title: "%s") {
                id
                title
                director
                rating
            }
        } 
    """ % title
    return request_graphql(f"http://{HOST}:{moviePort}/graphql", query)


@app.route("/moviesbyDirector/<movieDirector>", methods=['GET'])
def get_movie_byDirector(movieDirector):
    query = """
        query Movie_with_director {
            movie_with_director(_director: "%s") {
                id
                title
                director
                rating
            }
        }  
           """ % movieDirector

    return request_graphql(f"http://{HOST}:{moviePort}/graphql", query)

@app.route("/movies", methods=['POST'])
def create_movie():
    req = request.get_json()

    # check if all attributes are present in body
    attributes = ['id', 'title', 'director', 'rating']
    for attr in attributes:
        if attr not in req:
            return make_response(jsonify({'error': f'Attribute {attr} not present in body'}))

    query = """
    mutation Create_movie {
    create_movie(_id: "%s", _title: "%s", _director: "%s", _rating: %s) {
            id
            title
            director
            rating
        }
    }
    """ % (req['id'], req['title'], req['director'], req['rating'])

    return request_graphql(f"http://{HOST}:{moviePort}/graphql", query)


@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    query = """
    mutation Update_movie_rate {
        update_movie_rate(_id: "%s", _rate: %s) {
            id
            title
            director
            rating
        }
    }

    """ % (movieid, rate)
    return request_graphql(f"http://{HOST}:{moviePort}/graphql", query)


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):

    query = """
    mutation Delete_movie {
        delete_movie(_id: "%s") {
            id
            title
            director
            rating
        }
    }
    """ % movieid
    return request_graphql(f"http://{HOST}:{moviePort}/graphql", query)


# showtimes delegation

@app.route("/showtimes", methods=['GET'])
def get_schedule():
    return request_service(requests.get, f"http://{HOST}:{showtime}/showtimes")


@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    return request_service(requests.get, f"http://{HOST}:{showtime}/showtimes/{date}")


@app.route("/user/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    for user in users:
        if str(user["id"]) == str(id):
            return request_service(requests.get, f'http://{HOST}:{bookingPort}/bookings/{userid}')
    return make_response(jsonify({"error": "user ID don't exists"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)