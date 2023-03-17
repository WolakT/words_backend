from flask import Blueprint, current_app, request, jsonify

from app.dao.words import WordDAO

words_routes = Blueprint("words", __name__, url_prefix="/api/words")

# tag::list[]
@words_routes.get('/')
def get_words():
    # Extract pagination values from the request
    sort = request.args.get("sort", "name")
    type = request.args.get("type", "Adjective")
    order = request.args.get("order", "ASC")
    limit = request.args.get("limit", 6, type=int)
    skip = request.args.get("skip", 0, type=int)


    # Create a new MovieDAO Instance
    dao = WordDAO(current_app.driver)

    # Retrieve a paginated list of movies
    output = dao.all(type, sort, order, limit=limit, skip=skip)

    # Return as JSON
    return jsonify(output)
# end::list[]


#@movie_routes.get('/<movie_id>')
#def get_movie_details(movie_id):
#    user_id = current_user["sub"] if current_user != None else None
#
#    # Create a new MovieDAO Instance
#    dao = MovieDAO(current_app.driver)
#
#    # Get the Movie
#    movie = dao.find_by_id(movie_id, user_id)
#
#    return jsonify(movie)
#
#
