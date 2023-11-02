from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
import psycopg2

# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'AAAAAAAAAAA'  # Replace with a strong, random secret key

log_manager = LoginManager()
log_manager.init_app(app)

app.config['DATABASE_USER'] = 'fdggxsxy'
app.config['DATABASE_PASSWORD'] = 'fblPAJWqVJO-YUs7MyV6Itaje-NMrEA5'
app.config['DATABASE_NAME'] = 'fdggxsxy'
app.config['DATABASE_HOST'] = 'flora.db.elephantsql.com'
app.config['DATABASE_PORT'] = 5432


@app.route('/')  # domyślna strona startowa strona
def index():
    print('Started')
    return render_template("index.html")


@app.route("/authors")
def authors():
    return render_template("authors.html")


@app.route("/movies")
def movies():
    conn = connect_to_db()
    movies_list = get_data_about_movies()
    return render_template("Movies.html", movies=movies_list)


@app.route("/register", methods=["POST", "GET"])  # rejestracja konta
def register():
    if request.method == 'POST':  # jeżeli wysyłamy dane to rejestrujemy

        # Łączę sie z bazaą danych
        conn = connect_to_db()

        # pobiera dane z HTML form
        nick = request.form.get('username')  # czyta z html po atrybucie NAME
        password = request.form.get('password')
        account_type = request.form.get('account_type')
        account_type = int(account_type)

        # pobieranie id do konta z sekwencji
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT nextval('Account_ID_seq')""")
                account_id = cursor.fetchone()
                account_id = int(account_id[0])

        # automatycznie commituje do bazy jeśli nie ma błędu jeśli błąd to rollback
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""INSERT INTO accounts (account_id, nick, password, account_type_id) VALUES
                    ({account_id},'{nick}','{password}',{account_type})""")
                    flash('Account registered succesfully', 'info')
        except:
            flash('Failed to register account', 'error')

        # zamyka połącenie po skończeniu
        conn.close()

        print(f"Created account: Username: {nick} \n Password: {password} \n Account type: {account_type}")

        return render_template("Register.html")

    else:
        # jeżeli nie wysyłamy danych to po poprostu ładujemy stronę
        return render_template("Register.html")


@app.route("/prices")
def prices():
    return render_template("prices.html")


@app.route("/coming_soon")
def coming_soon():
    return render_template("Coming_soon.html")


def connect_to_db():
    try:
        conn = psycopg2.connect(
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            dbname=app.config['DATABASE_NAME'],
            host=app.config['DATABASE_HOST'],
            port=app.config['DATABASE_PORT']
        )
        print("Database connected successfully")
        return conn
    except Exception:
        print("Database not connected successfully")


class movie:
    def __init__(self, title, tier, genre):
        self.title = title
        self.tier = tier
        self.genre = genre


# TODO do modyfikacji
def get_data_about_movies(tier=None):
    conn = connect_to_db()
    cur = conn.cursor()

    if tier is None or tier == 4:
        cur.execute("""
                SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
                FROM movies Mo
                INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
                INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id
                ORDER BY Mo.account_type_id;
        """)
    elif tier == 3:
        cur.execute("""
                SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
                FROM movies Mo
                INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
                INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id 
                WHERE Mo.account_type_id < 4
                ORDER BY Mo.account_type_id;""")
    elif tier == 2:
        cur.execute("""
                SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
                FROM movies Mo
                INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
                INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id 
                WHERE Mo.account_type_id = 2
                ORDER BY Mo.account_type_id;
                """)
    else:
        print("Invalid 'tier' value:", tier)

    rows = cur.fetchall()

    returned_movies = []
    for data in rows:
        mov = movie(title=str(data[0]), genre=str(data[1]), tier=str(data[2]))
        returned_movies.append(mov)

    print('Data fetched successfully, total rows: ', len(returned_movies))
    return returned_movies


###########################################################
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@log_manager.user_loader
def load_user(user_id):
    user = User(user_id)
    return user


# todo zmienić na /login/<int:user_id> aby pozbyćsię parametórw w URL
@app.route("/login", methods=["POST", "GET"])  # logowanie na konto
def login():
    if request.method == 'POST':
        nick = request.form.get('nick')
        password = request.form.get('password')

        conn = connect_to_db()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT ac.account_id, ac.nick, ac.password, ac.account_type_id, at.account_type FROM accounts ac
                                    INNER JOIN account_types at ON at.account_type_id = ac.account_type_id
                 WHERE nick LIKE '{nick}' and password LIKE '{password}' """)
                user = cursor.fetchone()

                if user:
                    account_type_id = user[3]

                    if account_type_id == 1:

                        account_id = user[0]
                        account_type = user[4]

                        flash('Logged in successfully', 'info')
                        login_user(load_user(account_id))
                        users_data = get_data_about_users()

                        return redirect(url_for('admin_panel', nick=nick,
                                                account_type_id=int(account_type_id), account_type=account_type,
                                                users=users_data))

                    else:
                        account_id = user[0]
                        account_type_id = user[3]
                        account_type = user[4]

                        flash('Logged in successfully', 'info')

                        login_user(load_user(account_id))

                        movies_data = get_data_about_movies(tier=int(account_type_id))

                        return redirect(url_for('profile', nick=nick, movies=movies_data,
                                                account_type_id=int(account_type_id), account_type=account_type))
                else:
                    flash('Invalid username or password', 'error')

    return render_template("Login.html")


@app.route("/profile")
@login_required
def profile():
    nick = request.args.get('nick')
    account_type_id = request.args.get('account_type_id')
    account_type = request.args.get('account_type')

    returned_movies = get_data_about_movies(tier=int(account_type_id))

    return render_template("profile.html", nick=nick, movies=returned_movies, account_type=account_type)


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def delete_acocunt(account_id):
    conn = connect_to_db()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f""" DELETE from accounts where accounts.account_id = {account_id} """)


@app.route("/delete_account")
@login_required
def delete_account():
    user_id = current_user.get_id()
    delete_acocunt(user_id)
    logout_user()
    return redirect(url_for('index'))


@app.route("/admin_panel", methods=["POST", "GET"])
@login_required
def admin_panel():
    nick = request.args.get('nick')
    users_data = get_data_about_users()
    movie_data = get_data_about_movies()

    return render_template("admin_panel.html", nick=nick, users=users_data, movies=movie_data)


class Users_data:
    def __init__(self, id, nick, tier):
        self.tier = tier
        self.nick = nick
        self.id = id


def get_data_about_users():
    conn = connect_to_db()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f""" SELECT ACC.account_id, ACC.nick, acc_t.account_type, ACC.account_type_id
                                FROM accounts ACC
                                INNER JOIN account_types acc_t
                                ON ACC.account_type_id = acc_t.account_type_id
                                order by acc_t.account_type_id, ACC.account_id ; """)
            rows = cursor.fetchall()

    returned_users = []
    for data in rows:
        data = Users_data(id=int(data[0]), nick=str(data[1]), tier=str(data[2]))
        returned_users.append(data)

    print('Data fetched successfully, total rows: ', len(returned_users))
    return returned_users


# todo wybór genre w add movie nie jest dynamiczny i nie sprzężony z bazą danych, trzeba zdecydować czy zmienić

# todo user ma dostep do admin panel i to jest źle

@app.route('/add_movie', methods=["POST", "GET"])
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
            return redirect(url_for("add_movie", movies=movies_data))

        flash('Succesfully added new movie', 'info')
        return redirect(url_for("add_movie", movies=movies_data))
    else:
        return render_template("add_movie.html", movies=movies_data)

#TODO usuwanie filmu
@app.route('/admin_panel/delete_movie', methods=["POST", "GET"])
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
            return redirect(url_for("delete_movie", movies=movies_data))

        flash('Succesfully deleted movie', 'info')
        return redirect(url_for("delete_movie", movies=movies_data))
    else:
        return render_template("delete_movie.html", movies=movies_data)

#TODO modyfikacja filmu
@app.route('/admin_panel/modify_movie', methods=["POST", "GET"])
@login_required
def modify_movie():
    return render_template("modify_movie_panel.html")


if __name__ == '__main__':
    app.run(debug=True)
