from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
import psycopg2
from flask import Blueprint, render_template
from db import connect_to_db,get_data_about_movies

other_bp = Blueprint('other_routes', __name__)


@other_bp.route('/')  # domyślna strona startowa strona
def index():
    print('Started')
    return render_template("other_routes.index.html")


@other_bp.route("/authors")
def authors():
    return render_template("other_routes.authors.html")


@other_bp.route("/movies")
def movies():
    movies_list = get_data_about_movies()
    return render_template("other_routes.Movies.html", movies=movies_list)


@other_bp.route("/prices")
def prices():
    return render_template("other_routes.Prices.html")


@other_bp.route("/coming_soon")
def coming_soon():
    return render_template("other_routes.Coming_soon.html")