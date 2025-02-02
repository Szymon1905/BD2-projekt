import psycopg2
from config import *


def connect_to_db_online():  # tylko do testów
    try:
        conn = psycopg2.connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            dbname=DATABASE_NAME,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        print("Database connected successfully as admin")
        return conn
    except Exception:
        print("Database not connected successfully as admin")


"""
def connect_to_db_as_admin():
    try:
        conn = psycopg2.connect(
            user=DATABASE_USER_ADMIN,
            password=DATABASE_PASSWORD_ADMIN,
            dbname=DATABASE_NAME,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        print("Database connected successfully as admin")
        return conn
    except Exception:
        print("Database not connected successfully as admin")


# todo exception
def connect_to_db_as_user():
    try:
        conn = psycopg2.connect(
            user=DATABASE_USER_USER,
            password=DATABASE_PASSWORD_USER,
            dbname=DATABASE_NAME,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        print("Database connected successfully as user")
        return conn
    except Exception:
        print("Database not connected successfully as user")
"""


def connect_to_db_as_user():
    try:
        conn = psycopg2.connect(
            user=DATABASE_USER_A,
            password=DATABASE_PASSWORD_A,
            dbname=DATABASE_NAME,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        print("Database connected successfully")
        return conn
    except Exception:
        print("Database not connected successfully")


def connect_to_db_as_admin():
    try:
        conn = psycopg2.connect(
            user=DATABASE_USER_U,
            password=DATABASE_PASSWORD_U,
            dbname=DATABASE_NAME,
            host=DATABASE_HOST,
            port=DATABASE_PORT
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


def get_ALL_data_about_movies(sort):
    conn = connect_to_db_as_user()
    cur = conn.cursor()

    match sort:
        case 1:
            cur.execute("""
                SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
                FROM movies Mo
                INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
                INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id
                ORDER BY Mo.account_type_id;
                """)
        case 2:
            cur.execute("""
                 SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
                 FROM movies Mo
                 INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
                 INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id
                 ORDER BY Mo.movie_title;
                 """)
        case 3:
            cur.execute("""
                SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
                FROM movies Mo
                INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
                INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id
                ORDER BY Ge.genre_name;
                """)

    rows = cur.fetchall()

    returned_movies = []
    for data in rows:
        mov = movie(title=str(data[0]), genre=str(data[1]), tier=str(data[2]))
        returned_movies.append(mov)

    print('ALL Data fetched successfully, total rows: ', len(returned_movies))
    return returned_movies


# TODO do modyfikacji
def get_data_about_movies(tier=None):
    conn = connect_to_db_online()
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
                ORDER BY Mo.account_type_id;
                """)
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


class Users_data:
    def __init__(self, id, nick, tier):
        self.tier = tier
        self.nick = nick
        self.id = id


def get_data_about_users():
    conn = connect_to_db_online()
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
