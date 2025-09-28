from flask import Blueprint, render_template, request, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/display_event_details')
def display_event_details():
    return render_template('eventdetails.html')

@main_bp.route('/display_booking_history')
def display_booking_history():
    return render_template('userbookinghistory.html')

@main_bp.route('/create_update_event')
def create_update_event():
    return render_template('eventcreationupdate.html')

@main_bp.route('/login', methods = ['GET', 'POST'])
def login():
    email = request.values.get("email")
    passwd = request.values.get("pwd")
    print (f"Email: {email}\nPassword: {passwd}")
    # store email in session
    session['email'] = request.values.get('email')
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
    return 'User logged out'