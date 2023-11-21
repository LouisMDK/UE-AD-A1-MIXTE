import json


def get_all_movies(_, info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        newmovies = json.load(file)
        return newmovies['movies']


def create_movie(_, info, _id, _title, _director, _rating):
    newmovies = {}
    new = None
    with open('{}/data/movies.json'.format("."), "r") as file:
        newmovies = json.load(file)
        for movie in newmovies['movies']:
            if movie['id'] == _id:
                return new
        new = {'id': _id, 'title': _title, 'director': _director, 'rating': _rating}
        newmovies['movies'].append(new)
    
    if new is not None:
        with open('{}/data/movies.json'.format("."), "w") as wfile:
            # save change in data
            json.dump(newmovies, wfile)
    return new


def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def movie_with_title(_, info, _title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie


def movie_with_director(_, info, _director):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['director'] == _director:
                return movie


def delete_movie(_, info, _id):
    newmovies = {}
    deleted = None
    with (open('{}/data/movies.json'.format("."), "r") as rfile):
        movies = json.load(rfile)
        for index, movie in enumerate(movies['movies']):
            if movie['id'] == _id:
                deleted = movie
                del movies['movies'][index]
                newmovies = movies
                break
    if deleted is not None:
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
