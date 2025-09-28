from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from . models import User
from . import db
from flask_login import login_required, current_user
from . forms import check_upload_file, RegisterForm

user_bp = Blueprint('users', __name__, url_prefix='/user')

@user_bp.route('/display_booking_history')
@login_required
def display_booking_history():
    return render_template('userbookinghistory.html')

@user_bp.route('/create_update_event')
@login_required
def create_update_event():
    return render_template('eventcreationupdate.html')

# @user_bp.route('/register', methods = ['GET', 'POST'])
# def register():
#  print('Method type: ', request.method)
#  form = RegisterForm()
#  if form.validate_on_submit():
#   db_file_path = check_upload_file(form)
#   event = Event(
#     title=form.title.data, 
#     image=db_file_path, 
#     start_time=form.start_time.data,
#     end_time=form.end_time.data,
#     venue=form.venue.data,
#     vendor_names=form.vendor_names.data,
#     description=form.description.data,
#     total_tickets=form.total_tickets.data,
#     free_sampling=form.free_sampling.data,
#     provide_takeaway=form.provide_takeaway.data,
#     category_type=form.category_type.data
#     )
#   db.session.add(event)
#   db.session.commit()
#   flash('Successfully registered an account for FoodieVent', 'success')
#   return redirect(url_for('main.index'))
#   # Always end with redirect when form is valid
#  return render_template('register.html', form=form)