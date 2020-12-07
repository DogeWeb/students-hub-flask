from flask import render_template
from flask import Blueprint
from flask_login import current_user
from flask_login import login_required

from security.templates import get_templates_path

main_blueprint = Blueprint('main', __name__, )


@main_blueprint.route('/')
def home():
    return render_template(get_templates_path('main/index.html'), current_user=current_user)
