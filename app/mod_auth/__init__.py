# -*- coding: utf-8 -*-
from flask import Blueprint

blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='',
    template_folder='../templates',
    static_folder='../static'
)

from flask_login import LoginManager 
from app import app
from app.db.database import db_session
from app.db.models import User

login_manager  = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db = db_session()
    user = db.query(User).filter(User.id==int(user_id)).first()
    db.close()
    db_session.remove()
    return user

@app.teardown_appcontext
def cleanup(resp_or_exc):
    db_session.remove()

@app.teardown_request
def close_session(exception=None):
    db_session.remove()
