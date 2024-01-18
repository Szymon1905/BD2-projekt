from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.db import connect_to_db, get_data_about_movies, get_data_about_users
from app.users import admin_permission

admins_bp = Blueprint('admins', __name__)


@admins_bp.route("/admin_panel", methods=["POST", "GET"])
@admin_permission.require(http_exception=403)
@login_required
def admin_panel():
    nick = request.args.get('nick')
    users_data = get_data_about_users()
    movie_data = get_data_about_movies()

    return render_template("admin/admin_panel.html", nick=nick, users=users_data, movies=movie_data)


@admins_bp.route('/add_movie', methods=["POST", "GET"])
@admin_permission.require(http_exception=403)
@login_required
def add_movie():
    movies_data = get_data_about_movies()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        required_account_type = request.form.get('required_account_type')
        genre_id = request.form.get('genre_id')

        try:
            conn = connect_to_db()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(f""" INSERT INTO movies (movie_id, movie_title, account_type_id, description, genre_id)
                                        VALUES (nextval('account_id_seq'), '{title}', {required_account_type}, '{description}',{genre_id})""")
        except Exception:
            flash('Failed to add movie', 'error')
            return redirect(url_for("admins.add_movie", movies=movies_data))

        flash('Succesfully added new movie', 'info')
        return redirect(url_for("admins.add_movie", movies=movies_data))
    else:
        return render_template("admin/add_movie.html", movies=movies_data)


# TODO usuwanie filmu
@admins_bp.route('/admin_panel/delete_movie', methods=["POST", "GET"])
@admin_permission.require(http_exception=403)
@login_required
def delete_movie():
    movies_data = get_data_about_movies()
    if request.method == 'POST':
        title = request.form.get('title')

        try:
            conn = connect_to_db()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(f""" DELETE FROM MOVIES where movie_title LIKE '{title}' """)
                    cursor.execute(f""" DELETE FROM MOVIES where movie_title LIKE '{title}' """)
        except Exception:
            flash('Failed to delete movie', 'error')
            return redirect(url_for("admins.delete_movie", movies=movies_data))

        flash('Succesfully deleted movie', 'info')
        return redirect(url_for("admins.delete_movie", movies=movies_data))
    else:
        return render_template("admin/delete_movie.html", movies=movies_data)


# TODO modyfikacja filmu
@admins_bp.route('/admin_panel/modify_movie', methods=["POST", "GET"])
@admin_permission.require(http_exception=403)
@login_required
def modify_movie():
    movies_data = get_data_about_movies()
    if request.method == 'POST':
        title_selected = request.form.get('title_selector')
        title = request.form.get('title')
        description = request.form.get('description')
        required_account_type = int(request.form.get('required_account_type'))
        genre_id = int(request.form.get('genre_id'))

        query = f""" UPDATE MOVIES SET"""

        if title is not None:
            query = query + f""" movie_title = '{title}'"""

        if description == "":
            query = query + f""", description = '{description}'"""

        if required_account_type != 0:
            query = query + f""", account_type_id = {required_account_type}"""

        if genre_id != 0:
            query = query + f""", genre_id = {genre_id}"""

        query = query + f""" WHERE movie_title LIKE '{title_selected}'"""

        try:
            conn = connect_to_db()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
        except Exception:
            flash('Failed to modify movie', 'error')
            return redirect(url_for("admins.modify_movie", movies=movies_data))

        flash('Succesfully modified movie', 'info')
        return redirect(url_for("admins.modify_movie", movies=movies_data))
    else:
        return render_template("admin/modify_movie.html", movies=movies_data)
