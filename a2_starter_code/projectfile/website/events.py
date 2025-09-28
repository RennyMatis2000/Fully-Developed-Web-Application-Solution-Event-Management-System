from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from . models import Event, Comment, EventCategory, EventStatus
from . forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

event_bp = Blueprint('events', __name__, url_prefix='/events')

@event_bp.route('/<event_id>')
def show(event_id):
    event = db.session.scalar(db.select(Event).where(Event.event_id==event_id))
    # Generate comment form
    cform = CommentForm()
    return render_template('events/show.html', event=event, form=cform)

@event_bp.route('/create', methods = ['GET', 'POST'])
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

# UPDATE METHOD not implemented yet as must look into how to edit database data and overwrite

# @event_bp.route('/update', methods = ['GET', 'POST'])
# def update():
#   print('Method type: ', request.method)
#   form = EventForm()
#   if form.validate_on_submit():
#     db_file_path = check_upload_file(form)
#     event = Event(
#       title=form.title.data, 
#       image=db_file_path, 
#       start_time=form.start_time.data,
#       end_time=form.end_time.data,
#       venue=form.venue.data,
#       vendor_names=form.vendor_names,
#       description=form.description.data,
#       total_tickets=form.total_tickets.data,
#       free_sampling=form.free_sampling.data,
#       provide_takeaway=form.provide_takeaway.data,
#       category_type=form.category_type.data
#       )
#     db.session.add(event)
#     db.session.commit()
#     flash('Successfully created new Food and Drink Festival event', 'success')
#     return redirect(url_for('event.create'))
#    # Always end with redirect when form is valid
#   return render_template('events/create.html', form=form)

def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/img',secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  # save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@event_bp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(event_id):
  # here the form is created  form = CommentForm()
  form = CommentForm()
  event = db.session.scalar(db.select(Event).where(Event.event_id==event_id))
  if form.validate_on_submit():	#this is true only in case of POST method
    # read the current form
    event = Event(contents=form.contents.data, event=event)
    db.session.add(comment)
    db.session.commit()
    print("Your comment has been added", "success")
    
# using redirect sends a GET request to destination.show
  return redirect(url_for('event.show', event_id=event_id))

# def get_destination():
#   # creating the description of Brazil
#   b_desc = """Testing."""
#    # an image location
#   image_loc = 'static/img/MooncakeFestival.jpg'
# #   event = Event('event
#   # a comment
#   comment = Comment("Sam", "Visited during the olympics, was great", '2023-08-12 11:00:00')
#   destination.set_comments(comment)
#   comment = Comment("Bill", "free food!", '2023-08-12 11:00:00')
#   destination.set_comments(comment)
#   comment = Comment("Sally", "free face masks!", '2023-08-12 11:00:00')
#   destination.set_comments(comment)
#   return destination

# # Old get_event method which is replaced by get post method 
# def get_event(event_id):
#     event = Event(
#         event_id=event_id,  
#         title="Mid-Autumn Festival 2025",
#         image="static/img/MooncakeFestival.jpg",  
#         start_time=datetime(2025, 10, 6, 16, 0),
#         end_time=datetime(2025, 10, 6, 23, 0),
#         venue="The Mid-Autumn Festival 2025 is located at Chinatown Mall. 33 Duncan St, Fortitude Valley QLD 4006.",
#         vendor_names="The following Vendors will be participating in the Mid-Autumn Festival 2025: Sunnybank Jade Moon Bakery, Story Bridge Lotus & Yolk, Riverlight Mooncake House, Fortitude Valley Osmanthus Patisserie, South Bank Black Sesame Co.",
#         description="The Mid-Autumn Festival is a Chinese cultural food festival surrounding Mooncakes. Visit now at the Brisbane venue as many gather to celebrate Chinese food culture.",
#         total_tickets=200,
#         free_sampling=True,
#         provide_takeaway=True,
#         category_type=EventCategory.FOOD,
#         status=EventStatus.OPEN,
#         status_date=datetime.now,
#     )

#     event.comments = [
#         Comment(contents="I had the time of my life at the last Mid-Autumn Festival! Met some new friends and were meeting up again for this one.", comment_date=datetime(2025, 9, 1, 12, 0, tzinfo=timezone.utc),
#                 user_id=1, event_id=event_id),
#         Comment(contents="Is anyone else attending this? I was wondering if anyone wanted to do the Mooncake eating contest with me!!!", comment_date=datetime(2025, 9, 2, 9, 30, tzinfo=timezone.utc),
#                 user_id=2, event_id=event_id),
#     ]
#     return event