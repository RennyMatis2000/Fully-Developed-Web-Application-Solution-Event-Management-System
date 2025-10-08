from flask import Blueprint, render_template, request, session
from . models import Event, EventCategory
from . import db
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()    
    return render_template('index.html', events=events)

@main_bp.route('/food')
def food():
    events = db.session.scalars(
        db.select(Event).where(Event.category_type == EventCategory.FOOD)
    ).all()
    return render_template('index.html', events=events)

@main_bp.route('/drink')
def drink():
    events = db.session.scalars(
        db.select(Event).where(Event.category_type == EventCategory.DRINK)
    ).all()
    return render_template('index.html', events=events)

@main_bp.route('/cultural')
def cultural():
    events = db.session.scalars(
        db.select(Event).where(Event.category_type == EventCategory.CULTURAL)
    ).all()
    return render_template('index.html', events=events)

@main_bp.route('/dietary')
def dietary():
    events = db.session.scalars(
        db.select(Event).where(Event.category_type == EventCategory.DIETARY)
    ).all()
    return render_template('index.html', events=events)

@main_bp.route('/display_event_details')
def display_event_details():
    return render_template('eventdetails.html')

# @main_bp.route('/login', methods = ['GET', 'POST'])
# def login():
#     email = request.values.get("email")
#     passwd = request.values.get("pwd")
#     print (f"Email: {email}\nPassword: {passwd}")
#     # store email in session
#     session['email'] = request.values.get('email')
#     return render_template('login.html')

# @main_bp.route('/logout')
# def logout():
#     if 'email' in session:
#         session.pop('email')
#     return 'User logged out'

