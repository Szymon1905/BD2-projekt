from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, RoleNeed

from encryption import bcrypt
from extensions import log_manager, principal
from config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_HOST, DATABASE_PORT
from users import users_bp
from admins import admins_bp
from other_routes import other_bp

# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUS'  # Replace with a strong, random secret key

app.config['DATABASE_USER'] = DATABASE_USER
app.config['DATABASE_PASSWORD'] = DATABASE_PASSWORD
app.config['DATABASE_NAME'] = DATABASE_NAME
app.config['DATABASE_HOST'] = DATABASE_HOST
app.config['DATABASE_PORT'] = DATABASE_PORT

app.register_blueprint(users_bp)
app.register_blueprint(admins_bp)
app.register_blueprint(other_bp)

# rozszerzenia
log_manager.init_app(app)
principal.init_app(app)
bcrypt.init_app(app)


###########################################################
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))


if __name__ == '__main__':
    app.run(debug=False)


