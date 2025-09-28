from . import db
from datetime import datetime
import enum
from flask_login import UserMixin

class EventCategory(enum.Enum):
    FOOD = "Food"
    DRINK = "Drink"
    CULTURAL = "Cultural"
    DIETARY = "Dietary"

class EventStatus(enum.Enum):
    OPEN = "Open"
    INACTIVE = "Inactive"
    SOLDOUT = "Soldout"
    CANCELLED = "Cancelled"

class TicketType(enum.Enum):
    CHILD = "Child"
    ADULT = "Adult"

class User(db.Model, UserMixin):
    __tablename__ = "users"
    # Placeholder User data attributes subject to change
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    #Relationships to orders and comments from users
    orders = db.relationship("Order", backref="user")
    comments = db.relationship("Comment", backref="user")

    # string print method
    def __repr__(self):
        return f"Name: {self.username}"

class Event(db.Model):
    __tablename__ = "events"
    # Placeholder Event data attributes subject to change
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=True)   
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    vendor_names = db.Column(db.String(255))           
    description = db.Column(db.Text)
    total_tickets = db.Column(db.Integer, nullable=False)
    free_sampling = db.Column(db.Boolean, default=False)
    provide_takeaway = db.Column(db.Boolean, default=False)
    category_type = db.Column(db.Enum(EventCategory), nullable=False)
    status = db.Column(db.Enum(EventStatus), default=EventStatus.OPEN)
    status_date = db.Column(db.DateTime, default=datetime.now)

    # Relationships to orders and comments from events
    orders = db.relationship("Order", backref = "event")
    comments = db.relationship("Comment", backref = "event")

    # string print method
    def __repr__(self):
        return f"Name: {self.title}"

class Comment(db.Model):
    __tablename__ = "comments"
    # Placeholder Comment data attributes subject to change
    comment_id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, default=datetime.now)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"), nullable=False)

    # string print method
    def __repr__(self):
        return f"Name: {self.comment_id}"

class Order(db.Model):
    __tablename__ = "orders"
    # Placeholder Order data attributes subject to change
    order_id = db.Column(db.Integer, primary_key=True)
    booked = db.Column(db.Boolean, nullable=False, default=False)
    tickets_purchased = db.Column(db.Integer, nullable=False)  
    booking_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    ticket_type = db.Column(db.Enum(TicketType), nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"), nullable=False)

    # string print method
    def __repr__(self):
        return f"Name: {self.order_id}"