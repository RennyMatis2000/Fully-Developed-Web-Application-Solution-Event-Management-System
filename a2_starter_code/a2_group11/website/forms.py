from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, TelField, IntegerField, SelectField, BooleanField, PasswordField, DateTimeLocalField, DecimalField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, NumberRange
from . models import EventCategory, User
from . import db
from flask_wtf.file import FileRequired, FileField, FileAllowed
from flask import flash
from werkzeug.utils import secure_filename
import os

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

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

# Create an event or update an event
class EventForm(FlaskForm):
   title = StringField('Enter Title of this event', validators=[InputRequired()])
   description = StringField('Enter Description of this event', validators=[InputRequired()])
   image = FileField('Destination Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
   start_time = DateTimeLocalField("Start time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
   end_time = DateTimeLocalField("End time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
   venue = StringField("Venue", validators=[DataRequired()])
   vendor_names = StringField("List of vendors", validators=[InputRequired(), Length(max=255)])
   total_tickets = IntegerField("Total tickets", validators=[DataRequired()])
   ticket_price = DecimalField("Individual ticket price", places=2, validators=[InputRequired(), NumberRange(min=0)])
   free_sampling = BooleanField("Free sampling?")
   provide_takeaway = BooleanField("Provide takeaway?")
   category_type = SelectField("Category", choices=[(e.name, e.value) for e in EventCategory], validators=[DataRequired()])

  # Submission button
   submit = SubmitField("Create Event")

# Purchase ticket form
class PurchaseTicketForm(FlaskForm):
   tickets_purchased = IntegerField('Tickets Purchased', validators=[DataRequired()])

  # Submission button
   submit = SubmitField("Confirm Purchase")

# creates the login information
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name=StringField("First Name", validators=[InputRequired()])
    surname=StringField("Surname", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone=TelField("Contact Number", validators=[InputRequired("Please enter a valid phone number, which is exactly 10 digits"), Length(min=10, max=10)])
    address=StringField("Street Address", validators=[InputRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

# Create a user comment
class CommentForm(FlaskForm):
  contents = TextAreaField('Comment', validators=[InputRequired('Want to share your thoughts? Post a comment here')])
  submit = SubmitField('Create')

# Create an order form
# class OrderForm(FlaskForm):