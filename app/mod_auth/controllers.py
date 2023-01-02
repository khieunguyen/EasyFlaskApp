# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import logging
logger = logging.Logger(__name__)

from app.mod_auth import blueprint

from io import BytesIO
from app import app 
from app.db.models import User
from app.db.database import db_session  
from utils.two_factors import TwoFA 
from werkzeug.security import generate_password_hash, check_password_hash
import pyqrcode

from flask import render_template, redirect, url_for, session, request, flash, abort
from flask_login import login_required, current_user, login_user, logout_user

from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Bypass if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    if request.method=="GET":
        return render_template('auth/login.html', config=app.config )

    if request.method=='POST':
        email = request.values.get('email')
        password = request.values.get('password')
        remember =  request.values.get('remember')

        db = db_session()
        user = db.query(User).filter(
                    User.email==email
                ).first()
        db.close()
        db_session.remove()
        
        if (user is None) or (check_password_hash(user.password, password)==False):
            flash("Either email address or password is incorrect. Please try again.", "danger")
            return redirect(url_for("auth.login"))
        
        if (user.status in ['deleted', 'suspended']):
            flash("Your account has beed deleted or suspended. Please contact to admin.", "danger")
            return redirect(url_for("auth.login"))
        
        session['user_id']=user.id
        session['email'] = email
        session['remember']= remember

        # if 2FA is disabled => no need 2FA verification step
        if user.otp_status == 'disable':
            login_user(user, remember=session['remember'], duration=timedelta(days=7))
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for("home.index"))

        if (user.otp_status is None) or (user.otp_status == 'pending'):
            # switch to 2FA setup
            return redirect(url_for("auth.two_factor_setup") )
        else:
            # switch to 2FA login
            return redirect(url_for("auth.two_factor_login") )
        
@blueprint.route('/2fa-setup', methods=['GET'])
def two_factor_setup():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    else:
        # make sure the browser does not cache sensitive qr-code
        return render_template('auth/setup-2fa.html', config=app.config ), 200, {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'}

@blueprint.route('/2fa-login', methods=['GET', 'POST'])
def two_factor_login():
    if request.method == 'GET':
        if 'email' not in session:
            return redirect(url_for('auth.login'))
        else:
            # make sure the browser does not cache sensitive qr-code
            return render_template('auth/login-2fa.html', config=app.config ), 200, {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'}

    if request.method == 'POST':
        #  verify OTP
        verify_otp_token = request.form.get('otp')
        if verify_otp_token is not None:
            db = db_session()
            user = db.query(User).filter(
                        User.email==session['email']
                    ).first()
            db.close()
            db_session.remove()

            two_fa = TwoFA(email=user.email, otp_secret=user.otp_secret, issuer_name=app.config['SITE_NAME'])
            
            if two_fa.verify_totp(token=verify_otp_token):
                login_user(user, remember=session['remember'], duration=timedelta(days=7))
                next = request.args.get('next')
                if not is_safe_url(next):
                    return abort(400)
                return redirect(next or url_for('home.index'))
            else:
                flash("Incorrect token. Please try again.", "danger")
                return render_template('auth/login-2fa.html'), 200, {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'}


@blueprint.route('/2fa-qrcode')
def qrcode():
    
    if 'email' not in session:
        return abort(404)
    
    db = db_session()
    user = db.query(User).filter(
                User.email==session['email']
            ).first()
    if (user is None) or (user.status in ['deleted', 'suspended']):
        db.close()
        db_session.remove()
        return abort(404)

    # update otp_status to `enable`
    db.query(User).filter(
                User.id==session['user_id']
            ).update({User.status: 'active', 
                User.otp_status: 'enable',
                User.updated_at: datetime.now()})
    db.flush()
    db.commit()
    # render qrcode for 2FA
    two_fa = TwoFA(email=user.email, otp_secret=user.otp_secret, issuer_name=app.config['SITE_NAME'])
    
    db.close()
    db_session.remove()

    # for added security, remove email from session
    del session['email']

    url = pyqrcode.create(two_fa.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method  == 'GET':
        return render_template('auth/signup.html')

    email = request.form.get('email')
    password = request.form.get('password')
    
    # check if user exists
    db = db_session()
    user = db.query(User).filter(
                User.email==email
            ).first()
    db.close()
    db_session.remove()

    # if user exists
    if user is not None:
        flash('Email address already exists',  'danger')
        return redirect(url_for('auth.signup'))
    
    # create user
    two_fa = TwoFA(email=email)
    user  = User(
                email = email,
                password = generate_password_hash(password),
                status = 'pending',
                otp_secret = two_fa.otp_secret,
                otp_status = 'pending',
                created_at = datetime.now(),
                updated_at =  datetime.now()
            )
    db=db_session()
    db.add(user)
    db.flush()
    db.commit()
    db.close()
    db_session.remove()

    logger.debug(f"Create new user for '{email}'.")

    # redirect to login page
    return redirect(url_for('auth.login'))


@blueprint.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))


