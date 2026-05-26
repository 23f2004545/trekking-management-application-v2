from controller.extensions import db
from datetime import datetime


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    last_login_at = db.Column(db.DateTime)
    profile_pic = db.Column(db.String(225))
    blacklisted = db.Column(db.Boolean, default=False)
    
    # Relationships
    role = db.relationship('Role', secondary='user_roles', backref='user', lazy=True, uselist=False)
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    staff_profile = db.relationship('StaffProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    medical_record = db.relationship('MedicalRecord', backref='user', uselist=False, cascade='all, delete-orphan')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)



class Trek(db.Model):
    
    trek_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trek_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Moderate, Hard
    duration_days = db.Column(db.Integer, nullable=False)  # in days
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff_profile.staff_id'))
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Pending, Approved, Open, Closed, Completed
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    max_altitude = db.Column(db.Float)  # in meters
    price_per_person = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    # Relationships
    bookings = db.relationship('Booking', backref='trek', lazy=True, cascade='all, delete-orphan')
    assigned_staff = db.relationship('StaffProfile', backref='trek', foreign_keys=[assigned_staff_id])
 


class StaffProfile(db.Model):
    
    staff_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialization = db.Column(db.String(100))  # Guide, Medical Support, Logistics, etc.
    experience_years = db.Column(db.Integer)
    certification = db.Column(db.String(255))
    status = db.Column(db.String(20), default='Active', nullable=False)  # Active, Inactive, On Leave
    emergency_contact = db.Column(db.String(255))
    bio = db.Column(db.Text)
    

class Booking(db.Model):
    
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.trek_id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(20), default='Booked', nullable=False)  # Booked, Cancelled, Completed
    payment_status = db.Column(db.String(20), default='Pending', nullable=False)  # Pending, Paid, Refunded
    number_of_persons = db.Column(db.Integer, default=1, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    cancellation_reason = db.Column(db.Text)
    cancelled_at = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))  # Credit Card, Bank Transfer, Cash, etc.
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    
class MedicalRecord(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    trekker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    blood_group = db.Column(db.String(10), nullable=False) 
    diagonisis = db.Column(db.Text, nullable=True , default=None)     # Chronic illnesses (e.g., Asthma, Diabetes)
    allergies = db.Column(db.Text, nullable=True, default=None)       # Crucial emergency contact parameters (e.g., Peanuts, Penicillin)
    medications = db.Column(db.Text, nullable=True, default=None)     # Ongoing treatments required on-trail
    
    # Emergency Contact 
    emergency_name = db.Column(db.String(100), nullable=False)
    emergency_contact = db.Column(db.String(20), nullable=False)
    emergency_relation = db.Column(db.String(50), nullable=True) # Relation 
    
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class TrekReview(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.trek_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_profile.staff_id'), nullable=True) 

    trek_rating = db.Column(db.Integer, nullable=False)  
    staff_rating = db.Column(db.Integer, nullable=True) 
    trek_experience = db.Column(db.Text, nullable=False)    
    staff_experience = db.Column(db.Text, nullable=True)        
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship Matrices
    author = db.relationship('User', backref='trek_review')
    trek = db.relationship('Trek', backref='trek_review')
    reviewed_staff = db.relationship('StaffProfile', backref='trek_review', foreign_keys=[staff_id])