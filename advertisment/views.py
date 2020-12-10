from flask import Blueprint, render_template
from flask_login import login_required

from datatypes.utils import get_events, get_apartments
from decorators import check_confirmed

adv_blueprint = Blueprint('adv', __name__)


@adv_blueprint.route('/events')
@login_required
@check_confirmed
def events_list():
    return render_template('adv/events_list.html', events_list=get_events())


@adv_blueprint.route('/apartments')
@login_required
@check_confirmed
def apt_list():
    return render_template('adv/apartments_list.html', apts_list=get_apartments())

