from flask import Blueprint, current_app, request, jsonify

from app.dao.words import WordDAO

words_routes = Blueprint("words", __name__, url_prefix="/api/words")

# tag::list[]
@words_routes.route('/', methods=['POST', 'GET', 'DELETE'])
def get_words():
    dao = WordDAO(current_app.driver)
    if request.method == "GET":
        # Extract pagination values from the request
        sort = request.args.get("sort", "name")
        type = request.args.get("type", "Adjective")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)


#        # Create a new MovieDAO Instance
#        dao = WordDAO(current_app.driver)

        # Retrieve a paginated list of movies
        output = dao.all(type, sort, order, limit=limit, skip=skip)

        # Return as JSON
        return jsonify(output)
    if request.method == "DELETE":
        name = request.json.get("name")
        output = dao.remove(name)
        return jsonify(output)
    else:
        name = request.json.get("name")
        print(f"this is name {name}")
        type = request.json.get("type")
        print(f"this is type {type}")
        pl = request.json.get("pl")

        dao = WordDAO(current_app.driver)
        output = dao.add(type, name, pl)
        out = {'write': 'success'}
        return jsonify(out)
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
