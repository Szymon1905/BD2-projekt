from flask import Blueprint, render_template
from db import connect_to_db, get_data_about_movies, get_ALL_data_about_movies

other_bp = Blueprint('other_routes', __name__)


@other_bp.route('/')  # domyślna strona startowa strona
def index():
    print('Started')
    return render_template("other_routes/index.html")


@other_bp.route("/authors")
def authors():
    return render_template("other_routes/authors.html")


@other_bp.route("/movies", methods=["POST", "GET"])
def movies():
    if request.method == 'POST':
        sort_type = int(request.form.get('sort'))
        movies_list = get_ALL_data_about_movies(sort=sort_type)
        return render_template("other_routes/Movies.html", movies=movies_list)
    else:
        movies_list = get_data_about_movies()
        return render_template("other_routes/Movies.html", movies=movies_list)

"""
@other_bp.route("/prices")
def prices():
    return render_template("other_routes/Prices.html")


@other_bp.route("/coming_soon")
def coming_soon():
    return render_template("other_routes/Coming_soon.html")
"""
