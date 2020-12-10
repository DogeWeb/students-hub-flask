import os

from flask import Flask, render_template, jsonify, g
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_required
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

import projconfig

app = Flask(__name__)
app.config.from_object(projconfig.BaseConfig)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)

from main.views import main_blueprint
from user.views import user_blueprint
from meetings.views import meetings_blueprint
from notes.views import notes_blueprint
from advertisment.views import adv_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(meetings_blueprint)
app.register_blueprint(notes_blueprint)
app.register_blueprint(adv_blueprint)

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    from datatypes.utils import get_user_by_id
    return get_user_by_id(user_id)


# @app.route('/activate_db')
# def activate_db():
#     return db.create_all()

@app.route('/get_adv_image/<filename>')
@login_required
def get_adv_image(filename):
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'adv'), filename)


@app.route('/_get_current_user')
@login_required
def get_current_user():
    return jsonify(email=current_user.email,
                   id=current_user.id)


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500


if __name__ == '__main__':
    app.run()
