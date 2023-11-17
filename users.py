from flask import request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template
from flask_principal import RoleNeed, Permission, Identity, identity_changed
import encryption
from db import connect_to_db_online, get_data_about_movies, get_data_about_users
from extensions import log_manager
from main import app
from flask_login import UserMixin

users_bp = Blueprint('users', __name__)

admin_role = RoleNeed('admin')
user_role = RoleNeed('user')

# Define permissions
admin_permission = Permission(admin_role)
user_permission = Permission(user_role)


@users_bp.route("/register", methods=["POST", "GET"])  # rejestracja konta
def register():
    if request.method == 'POST':  # jeżeli wysyłamy dane to rejestrujemy

        # Łączę sie z bazaą danych
        conn = connect_to_db_online()

        # pobiera dane z HTML form
        nick = request.form.get('username')  # czyta z html po atrybucie NAME
        password = request.form.get('password')
        account_type = request.form.get('account_type')
        account_type = int(account_type)

        password = encryption.hash_password(password)

        # pobieranie id do konta z sekwencji
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT nextval('Account_ID_seq')""")
                account_id = cursor.fetchone()
                account_id = int(account_id[0])

        # automatycznie commituje do bazy jeśli nie ma błędu jeśli błąd to rollback
        query = f"""INSERT INTO accounts (account_id, nick, password, account_type_id) VALUES
                            ({account_id},'{nick}','{password}',{account_type})"""
        print(query)

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    flash('Account registered succesfully', 'info')
        except:
            flash('Failed to register account', 'error')

        # zamyka połącenie po skończeniu
        conn.close()

        print(f"Created account: Username: {nick} \n Password: {password} \n Account type: {account_type}")

        return render_template("users/register.html")

    else:
        # jeżeli nie wysyłamy danych to po poprostu ładujemy stronę
        return render_template("users/register.html")


class User(UserMixin):
    def __init__(self, user_id, access_level):
        self.id = user_id
        self.access_level = access_level


@log_manager.user_loader
def load_user(user_id):
    conn = connect_to_db_online()
    get_level = f"""SELECT account_type_id from accounts
                             WHERE account_id = '{user_id}' """
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(get_level)
            access_level = cursor.fetchone()[0]
    user = User(user_id, access_level)
    return user


# todo zmienić na /login/<int:user_id> aby pozbyćsię parametórw w URL
@users_bp.route("/login", methods=["POST", "GET"])  # logowanie na konto
def login():
    if request.method == 'POST':
        nick = request.form.get('nick')
        entered_password = request.form.get('password')

        conn = connect_to_db_online()

        get_hash = f"""SELECT password from accounts
                         WHERE nick LIKE '{nick}' """

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(get_hash)
                user = cursor.fetchone()

                if user:
                    hashed_password_from_db = user[0]
                    if not encryption.bcrypt.check_password_hash(hashed_password_from_db, entered_password):
                        flash('Invalid username or password', 'error')
                        return render_template("users/login.html")
                else:
                    flash('Invalid username or password', 'error')
                    return render_template("users/login.html")

        query = f"""SELECT ac.account_id, ac.account_type_id, at.account_type FROM accounts ac
                                    INNER JOIN account_types at ON at.account_type_id = ac.account_type_id
                 WHERE ac.nick LIKE '{nick}' """

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                user = cursor.fetchone()

                if user:
                    account_type_id = user[1]
                    account_id = user[0]
                    account_type = user[2]

                    if account_type_id == 1:
                        # he got here correctly

                        identity = Identity(account_id)
                        identity.provides.add(RoleNeed('admin'))
                        identity_changed.send(app, identity=identity)

                        login_user(load_user(account_id))
                        users_data = get_data_about_users()
                        return redirect(url_for('admins.admin_panel', nick=nick,
                                                account_type_id=int(account_type_id), account_type=account_type,
                                                users=users_data))
                    else:
                        print("USER TU WLAZŁ ")
                        flash('Logged in successfully', 'info')
                        login_user(load_user(account_id))
                        movies_data = get_data_about_movies(tier=int(account_type_id))
                        return redirect(url_for('users.profile', nick=nick, movies=movies_data,
                                                account_type_id=int(account_type_id), account_type=account_type))
                else:
                    flash('Invalid username or password', 'error')

    return render_template("users/login.html")


@users_bp.route("/profile")
@login_required
def profile():
    nick = request.args.get('nick')
    account_type_id = request.args.get('account_type_id')
    account_type = request.args.get('account_type')

    returned_movies = get_data_about_movies(tier=int(account_type_id))

    return render_template("users/profile.html", nick=nick, movies=returned_movies, account_type=account_type)


@users_bp.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('other_routes.index'))


def delete_acocunt(account_id):
    conn = connect_to_db_online()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f""" DELETE from accounts where accounts.account_id = {account_id} """)


@users_bp.route("/delete_account")
@login_required
def delete_account():
    user_id = current_user.get_id()
    delete_acocunt(user_id)
    logout_user()
    return redirect(url_for('other_routes.index'))
