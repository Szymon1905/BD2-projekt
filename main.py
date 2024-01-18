from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, RoleNeed
from config import Config

from app.encryption import bcrypt
from app.extensions import log_manager, principal
from app.users import users_bp
from app.admins import admins_bp
from app.other_routes import other_bp

# Create the Flask application
app = Flask(__name__, static_folder="app/static", template_folder="app/templates")
app.config.from_object(Config)

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
    app.run(debug=True)


