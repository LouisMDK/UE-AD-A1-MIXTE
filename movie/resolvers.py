import json


def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def movie_with_title(_, info, title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == title:
                return movie

def movie_with_director(_, info, director):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['director'] == director:
                return movie


def delete_movie(_, info, _id):
    newmovies = {}
    deleted = {}
    with (open('{}/data/movies.json'.format("."), "r") as rfile):
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                deleted = movie
                del movie
                newmovies = movies
                break
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return deleted


def update_movie_rate(_, info, _id, _rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
                break
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors


def actor_with_id(_, info, _id):
    with open('{}/data/actors.json'.format("."), "r") as rfile:
        actors = json.load(rfile)
        for actor in actors['actors']:
            if actor['id'] == _id:
                return actor
