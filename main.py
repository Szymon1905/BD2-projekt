from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
import psycopg2

# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'AAAAAAAAAAA'  # Replace with a strong, random secret key

log_manager = LoginManager()
log_manager.init_app(app)

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "famished"
DB_HOST = "localhost"
DB_PORT = "5432"


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
    movies_list = get_data_about_movies(conn)
    return render_template("Movies.html", movies=movies_list)


@app.route("/register", methods=["POST", "GET"])  # rehjestracja konta
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
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
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
def get_data_about_movies(conn):
    cur = conn.cursor()
    cur.execute("""
    SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
    FROM movies Mo
    INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
    INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id order by Mo.account_type_id;
    """)

    rows = cur.fetchall()


    returned_movies = []
    for data in rows:
        mov = movie(title=str(data[0]), genre=str(data[1]), tier=str(data[2]))
        returned_movies.append(mov)

    print('Data fetched successfully')
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


@app.route("/login", methods=["POST", "GET"])  # logowanie na konto
def login():
    if request.method == 'POST':
        nick = request.form.get('nick')
        password = request.form.get('password')

        conn = connect_to_db()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT account_id, nick, password FROM accounts
                 WHERE nick LIKE '{nick}' and password LIKE '{password}' """)
                user = cursor.fetchone()
                if user:
                    flash('Logged in successfully', 'info')
                    account_id = user[0]
                    login_user(load_user(account_id))
                    return redirect(url_for('profile'))
                else:
                    flash('Invalid username or password', 'error')

    return render_template("Login.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
