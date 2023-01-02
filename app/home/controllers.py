# -*- coding: utf-8 -*-
from os import path
from app.home import blueprint
from flask import render_template, session, g, send_from_directory
from app import app

from flask_login import login_required, current_user

@blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@blueprint.route('/')
#@login_required
def index():
    return render_template('home/index.html', config=app.config)

@blueprint.before_app_request
def load_logged_in_user():
    user_email = session.get('email')

    if user_email is None:
        g.email = None
    else:
        g.email = user_email
        # check database
