from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, TelField, IntegerField, SelectField, BooleanField, PasswordField, DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo
from . models import EventCategory
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

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
   free_sampling = BooleanField("Free sampling?")
   provide_takeaway = BooleanField("Provide takeaway?")
   category_type = SelectField("Category", choices=[(e.name, e.value) for e in EventCategory], validators=[DataRequired()])

  # Submission button
   submit = SubmitField("Create Event")

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")


 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    phone=TelField("Phone Number", validators=[InputRequired("Please enter a valid phone number, which is exactly 10 digits"), Length(min=10, max=10)])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

# Create a user comment
class CommentForm(FlaskForm):
  contents = TextAreaField('Comment', validators=[InputRequired('Want to share your thoughts? Post a comment here')])
  submit = SubmitField('Create')

# Create an order form
# class OrderForm(FlaskForm):