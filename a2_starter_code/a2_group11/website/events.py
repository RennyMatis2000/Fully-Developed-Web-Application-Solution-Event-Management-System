from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from . models import Event, Comment, EventCategory, EventStatus
from . forms import EventForm, CommentForm, check_upload_file
from . import db
from flask_login import login_required, current_user

event_bp = Blueprint('events', __name__, url_prefix='/events')

@event_bp.route('/<event_id>')
def show(event_id):
    event = db.session.scalar(db.select(Event).where(Event.id==event_id))
    # Generate comment form
    cform = CommentForm()
    return render_template('events/show.html', event=event, form=cform)

# Create event method

@event_bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    event = Event(
      title=form.title.data, 
      image=db_file_path, 
      start_time=form.start_time.data,
      end_time=form.end_time.data,
      venue=form.venue.data,
      vendor_names=form.vendor_names.data,
      description=form.description.data,
      total_tickets=form.total_tickets.data,
      free_sampling=form.free_sampling.data,
      provide_takeaway=form.provide_takeaway.data,
      category_type=form.category_type.data
      )
    db.session.add(event)
    db.session.commit()
    flash('Successfully created new Food and Drink Festival event', 'success')
    return redirect(url_for('events.create'))
   # Always end with redirect when form is valid
  return render_template('events/create.html', form=form)

# Update event method

@event_bp.route('/update<event_id>', methods = ['GET', 'POST'])
@login_required
def update(event_id):
  print('Method type: ', request.method)
  event = db.session.get(Event, event_id)
  form = EventForm(obj=event)
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    event = Event(
        title=form.title.data, 
        image=db_file_path, 
        start_time=form.start_time.data,
        end_time=form.end_time.data,
        venue=form.venue.data,
        vendor_names=form.vendor_names,
        description=form.description.data,
        total_tickets=form.total_tickets.data,
        free_sampling=form.free_sampling.data,
        provide_takeaway=form.provide_takeaway.data,
        category_type=form.category_type.data
      )
      
    db.session.add(event)
    db.session.commit()
    flash('Successfully updated Food and Drink Festival event', 'success')
    return redirect(url_for('event.update'))
    # Always end with redirect when form is valid
  return render_template('events/update.html', form=form)

# Post comment method

@event_bp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(event_id):
  # here the form is created  form = CommentForm()
  form = CommentForm()
  event = db.session.scalar(db.select(Event).where(Event.id==event_id))
  if form.validate_on_submit():	#this is true only in case of POST method
    # read the current form
    event = Event(contents=form.contents.data, event=event)
    db.session.add(comment)
    db.session.commit()
    print("Your comment has been added", "success")
    
# using redirect sends a GET request to destination.show
  return redirect(url_for('event.show', event_id=event_id))