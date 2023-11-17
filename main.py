from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
import psycopg2

from encryption import bcrypt
from extensions import log_manager, principal
from config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_HOST, DATABASE_PORT

# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'AAAAAAAAAAA'  # Replace with a strong, random secret key

app.config['DATABASE_USER'] = DATABASE_USER
app.config['DATABASE_PASSWORD'] = DATABASE_PASSWORD
app.config['DATABASE_NAME'] = DATABASE_NAME
app.config['DATABASE_HOST'] = DATABASE_HOST
app.config['DATABASE_PORT'] = DATABASE_PORT


from users import users_bp
from admins import admins_bp
from other_routes import other_bp

app.register_blueprint(users_bp)
app.register_blueprint(admins_bp)
app.register_blueprint(other_bp)

# rozszerzenia
log_manager.init_app(app)
principal.init_app(app)
bcrypt.init_app(app)



if __name__ == '__main__':
    app.run(debug=True)

















###########################################################












# todo wybór genre w add movie nie jest dynamiczny i nie sprzężony z bazą danych, trzeba zdecydować czy zmienić

# todo user ma dostep do admin panel i to jest źle

