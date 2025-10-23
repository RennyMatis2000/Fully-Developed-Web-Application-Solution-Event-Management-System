from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db
from . events import live_status

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email= login_form.email.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email==email))
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                live_status()
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,   
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        print('Successfully registered')
        return redirect(url_for('auth.login'))
    return render_template('user.html', form=form, heading = 'Register an Account')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    live_status()
    return redirect(url_for('main.index'))