"""
Demo Service: Seed Data, Auto-Reseed, and Safe Simulation Helpers
Provides dedicated showcase profiles for Admin, Staff, and Trekkers with self-healing data.
"""

import logging
import traceback
from datetime import datetime, timezone, timedelta
from controller.extensions import db, bcrypt
from controller.models import (
    User, Role, StaffProfile, MedicalRecord,
    Trek, TrekImage, Booking, Review, DispatchTicket
)

logger = logging.getLogger(__name__)


DEMO_USERS = {
    "admin": {
        "email": "demo.admin@apex.com",
        "name": "Apex Admin (Demo)",
        "password": "DemoPassword123!",
        "contact": "9999990001",
        "profile_pic": "/static/Profile_pics/admin.png",
        "role": "admin"
    },
    "trek_staff": {
        "email": "demo.staff1@apex.com",
        "name": "Tenzing Norgay (Demo)",
        "password": "DemoPassword123!",
        "contact": "9999990002",
        "profile_pic": "/static/Profile_pics/trek_staff.png",
        "role": "trek_staff",
        "specialization": "High-Altitude Mountain Guide",
        "experience_years": 8,
        "certification": "UIAGM/IFMGA",
        "emergency_contact": "9999990010"
    },
    "staff2": {
        "email": "demo.staff2@apex.com",
        "name": "Bachendri Pal (Demo)",
        "password": "DemoPassword123!",
        "contact": "9999990003",
        "profile_pic": "/static/Profile_pics/trek_staff.png",
        "role": "trek_staff",
        "specialization": "Wilderness First Responder & Logistics",
        "experience_years": 6,
        "certification": "WFR / IMF Lead",
        "emergency_contact": "9999990020"
    },
    "trekker": {
        "email": "demo.trekker1@apex.com",
        "name": "Alex Explorer (Demo)",
        "password": "DemoPassword123!",
        "contact": "9999990004",
        "profile_pic": "/static/Profile_pics/trekker.png",
        "role": "trekker",
        "blood_group": "O+",
        "diagnosis": "None",
        "allergies": "None",
        "medications": "None",
        "emergency_name": "Sarah Explorer",
        "emergency_contact": "9999990030",
        "emergency_relation": "Spouse"
    },
    "trekker2": {
        "email": "demo.trekker2@apex.com",
        "name": "Maya Climber (Demo)",
        "password": "DemoPassword123!",
        "contact": "9999990005",
        "profile_pic": "/static/Profile_pics/trekker.png",
        "role": "trekker",
        "blood_group": "A+",
        "diagnosis": "Mild Seasonal Asthma",
        "allergies": "Penicillin",
        "medications": "Albuterol Inhaler",
        "emergency_name": "Rohan Climber",
        "emergency_contact": "9999990040",
        "emergency_relation": "Brother"
    }
}


def is_demo_user(user=None):
    """
    Checks whether the current request/session or user model instance is a demo account.
    Prioritizes the JWT additional claims ('is_demo') so any demo token is strictly isolated.
    """
    try:
        from flask_jwt_extended import get_jwt
        claims = get_jwt()
        if claims and claims.get('is_demo'):
            return True
    except Exception:
        pass

    if not user:
        return False

    if isinstance(user, str):
        email = user.lower()
        return email.startswith('demo.') or '@demo.' in email or '.demo.' in email or 'demo' in email

    email = (getattr(user, 'email', '') or '').lower()
    name = (getattr(user, 'name', '') or '').lower()
    return (
        email.startswith('demo.') or
        '@demo.' in email or
        '.demo.' in email or
        'demo' in email or
        '(demo)' in name or
        'demo' in name
    )


def is_demo_target(entity):
    """
    Checks whether a specific database entity (User, Trek, Booking, Ticket) is a demo record.
    NOTE: This strictly inspects the record itself, NOT the active JWT claims, ensuring real user/staff
    records are never mistaken for demo targets.
    """
    if not entity:
        return False

    if isinstance(entity, User):
        email = (getattr(entity, 'email', '') or '').lower()
        name = (getattr(entity, 'name', '') or '').lower()
        return (
            email.startswith('demo.') or
            '@demo.' in email or
            '.demo.' in email or
            'demo' in email or
            '(demo)' in name
        )

    if isinstance(entity, Trek):
        return '(demo)' in (entity.trek_name or '').lower()

    if isinstance(entity, Booking):
        return is_demo_target(entity.user) or is_demo_target(entity.trek)

    if isinstance(entity, DispatchTicket):
        return '(demo)' in (entity.subject or '').lower() or is_demo_target(entity.author)

    return False


def seed_or_reset_demo_data(target_role=None):
    """
    Ensures all baseline demo data (Admin, 2 Staff, 2 Trekkers, 3 Treks, Bookings, Tickets)
    exist and are intact. Automatically restores any deleted or corrupted demo records.
    """
    try:
        return _do_seed_demo_data(target_role)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to seed demo data: {e}\n{traceback.format_exc()}")
        raise e


def _do_seed_demo_data(target_role=None):
    roles = {
        'admin': Role.query.filter_by(name='admin').first(),
        'trek_staff': Role.query.filter_by(name='trek_staff').first(),
        'trekker': Role.query.filter_by(name='trekker').first()
    }

    # 1. Seed or Restore Users
    user_instances = {}
    for key, spec in DEMO_USERS.items():
        role_obj = roles.get(spec['role'])
        user = User.query.filter_by(email=spec['email']).first()

        if not user:
            user = User(
                name=spec['name'],
                email=spec['email'],
                password=bcrypt.generate_password_hash(spec['password']).decode('utf-8'),
                contact=spec['contact'],
                profile_pic=spec['profile_pic'],
                role=role_obj,
                is_active=True,
                blacklisted=False
            )

            user.role = role_obj
                
            db.session.add(user)
            db.session.flush()
        else:
            # Ensure restored to pristine active state
            user.name = spec['name']
            user.is_active = True
            user.blacklisted = False
            
            if user.role != role_obj:
                user.role = role_obj

        # Staff Profile
        if spec['role'] == 'trek_staff':
            sp = StaffProfile.query.filter_by(user_id=user.id).first()
            if not sp:
                sp = StaffProfile(
                    user_id=user.id,
                    specialization=spec.get('specialization', 'Mountain Guide'),
                    experience_years=spec.get('experience_years', 5),
                    certification=spec.get('certification', 'Certified Guide'),
                    status='Active',
                    emergency_contact=spec.get('emergency_contact', '9999990000'),
                    bio='Expedition guide with extensive alpine leadership experience.'
                )
                db.session.add(sp)
            else:
                sp.status = 'Active'

        # Medical Record for Trekker
        if spec['role'] == 'trekker':
            mr = MedicalRecord.query.filter_by(trekker_id=user.id).first()
            if not mr:
                mr = MedicalRecord(
                    trekker_id=user.id,
                    blood_group=spec.get('blood_group', 'O+'),
                    diagnosis=spec.get('diagnosis', 'None'),
                    allergies=spec.get('allergies', 'None'),
                    medications=spec.get('medications', 'None'),
                    emergency_name=spec.get('emergency_name', 'Emergency Contact'),
                    emergency_contact=spec.get('emergency_contact', '9999990000'),
                    emergency_relation=spec.get('emergency_relation', 'Family')
                )
                db.session.add(mr)

        user_instances[key] = user

    db.session.commit()

    # Staff guide User IDs (Trek.assigned_staff_id links to User.id)
    staff1_user = user_instances['trek_staff']
    staff2_user = user_instances['staff2']

    # 2. Seed or Restore 3 Demo Treks
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    demo_treks_specs = [
        {
            "name": "Hampta Pass Expedition (Demo)",
            "location": "Himachal Pradesh",
            "difficulty": "Moderate",
            "duration_days": 5,
            "available_slots": 12,
            "price_per_person": 7500.0,
            "max_altitude": 4270.0,
            "status": "Open",
            "start_date": now + timedelta(days=12),
            "end_date": now + timedelta(days=17),
            "assigned_staff_id": staff1_user.id,
            "description": "Cross from the lush Kullu valley to the arid desert of Lahaul across Hampta Pass."
        },
        {
            "name": "Rohtang Valley Trail (Demo)",
            "location": "Himachal Pradesh",
            "difficulty": "Easy",
            "duration_days": 3,
            "available_slots": 15,
            "price_per_person": 4500.0,
            "max_altitude": 3978.0,
            "status": "Open",
            "start_date": now + timedelta(days=20),
            "end_date": now + timedelta(days=23),
            "assigned_staff_id": staff2_user.id,
            "description": "Scenic alpine meadows with panoramic views of the Pir Panjal mountain range."
        },
        {
            "name": "Pin Parvati Pass (Demo)",
            "location": "Himachal Pradesh",
            "difficulty": "Hard",
            "duration_days": 8,
            "available_slots": 8,
            "price_per_person": 14000.0,
            "max_altitude": 5319.0,
            "status": "Completed",
            "start_date": now - timedelta(days=35),
            "end_date": now - timedelta(days=27),
            "assigned_staff_id": staff1_user.id,
            "description": "Challenging trans-Himalayan crossover expedition connecting Parvati and Pin valleys."
        }
    ]

    trek_instances = []
    for t_spec in demo_treks_specs:
        trek = Trek.query.filter_by(trek_name=t_spec['name']).first()
        if not trek:
            trek = Trek(
                trek_name=t_spec['name'],
                location=t_spec['location'],
                difficulty=t_spec['difficulty'],
                duration_days=t_spec['duration_days'],
                available_slots=t_spec['available_slots'],
                price_per_person=t_spec['price_per_person'],
                max_altitude=t_spec['max_altitude'],
                status=t_spec['status'],
                start_date=t_spec['start_date'],
                end_date=t_spec['end_date'],
                assigned_staff_id=t_spec['assigned_staff_id'],
                description=t_spec['description'],
                is_deleted=False
            )
            db.session.add(trek)
            db.session.flush()

            # Add default gallery images for this trek
            for i in range(4):
                img = TrekImage(
                    trek_id=trek.trek_id,
                    image_url=f"/static/Treks/default_trek.jpg"
                )
                db.session.add(img)
        else:
            trek.is_deleted = False
            trek.status = t_spec['status']
            trek.available_slots = t_spec['available_slots']
            trek.assigned_staff_id = t_spec['assigned_staff_id']
            if not trek.images or len(trek.images) < 4:
                TrekImage.query.filter_by(trek_id=trek.trek_id).delete()
                for i in range(4):
                    db.session.add(TrekImage(trek_id=trek.trek_id, image_url="/static/Treks/default_trek.jpg"))

        trek_instances.append(trek)

    db.session.commit()

    # 3. Seed or Restore Bookings (Active & Completed)
    trekker1 = user_instances['trekker']
    trekker2 = user_instances['trekker2']

    demo_bookings_specs = [
        # Trekker 1 on Trek 1 (Active)
        {
            "user_id": trekker1.id,
            "trek": trek_instances[0],
            "status": "Booked",
            "payment_status": "Paid",
            "number_of_persons": 2,
            "total_amount": 15000.0
        },
        # Trekker 1 on Trek 3 (Completed)
        {
            "user_id": trekker1.id,
            "trek": trek_instances[2],
            "status": "Completed",
            "payment_status": "Paid",
            "number_of_persons": 1,
            "total_amount": 14000.0
        },
        # Trekker 2 on Trek 2 (Active)
        {
            "user_id": trekker2.id,
            "trek": trek_instances[1],
            "status": "Booked",
            "payment_status": "Paid",
            "number_of_persons": 1,
            "total_amount": 4500.0
        },
        # Trekker 2 on Trek 3 (Completed)
        {
            "user_id": trekker2.id,
            "trek": trek_instances[2],
            "status": "Completed",
            "payment_status": "Paid",
            "number_of_persons": 2,
            "total_amount": 28000.0
        }
    ]

    for b_spec in demo_bookings_specs:
        existing_booking = Booking.query.filter_by(
            user_id=b_spec['user_id'],
            trek_id=b_spec['trek'].trek_id
        ).first()

        if not existing_booking:
            b = Booking(
                user_id=b_spec['user_id'],
                trek_id=b_spec['trek'].trek_id,
                status=b_spec['status'],
                payment_status=b_spec['payment_status'],
                number_of_persons=b_spec['number_of_persons'],
                total_amount=b_spec['total_amount'],
                snapshot_start_date=b_spec['trek'].start_date,
                snapshot_end_date=b_spec['trek'].end_date,
                snapshot_duration_days=b_spec['trek'].duration_days,
                snapshot_staff=b_spec['trek'].assigned_staff_id or staff1_user.id
            )
            db.session.add(b)
        else:
            existing_booking.status = b_spec['status']
            existing_booking.payment_status = b_spec['payment_status']

    # 4. Seed or Restore Demo Tickets
    ticket1 = DispatchTicket.query.filter_by(subject="Trail Crampons Inquiry (Demo)").first()
    if not ticket1:
        ticket1 = DispatchTicket(
            author_id=trekker1.id,
            subject="Trail Crampons Inquiry (Demo)",
            message="Do we require microspikes or full crampons for the Hampta Pass snow section?",
            priority="Routine",
            status="Pending"
        )
        db.session.add(ticket1)

    ticket2 = DispatchTicket.query.filter_by(subject="Medical Oxygen Replenishment (Demo)").first()
    if not ticket2:
        ticket2 = DispatchTicket(
            author_id=user_instances['staff2'].id,
            subject="Medical Oxygen Replenishment (Demo)",
            message="Basecamp 2 oxygen tanks require annual hydrostatic test verification.",
            priority="Urgent",
            status="Resolved",
            admin_response="Inspection authorized and depot replacement cylinders dispatched."
        )
        db.session.add(ticket2)

    # 5. Seed or Restore Demo Review on Completed Trek
    staff1_profile = StaffProfile.query.filter_by(user_id=staff1_user.id).first()
    review = Review.query.filter_by(user_id=trekker1.id, trek_id=trek_instances[2].trek_id).first()
    if not review:
        review = Review(
            user_id=trekker1.id,
            trek_id=trek_instances[2].trek_id,
            staff_id=staff1_profile.staff_id if staff1_profile else None,
            trek_rating=5,
            staff_rating=5,
            trek_experience="Breathtaking high-altitude traverse across glacial moraine. Top-notch safety compliance!",
            staff_experience="Tenzing set a comfortable acclimatization pace and kept everyone in good spirits."
        )
        db.session.add(review)

    db.session.commit()

    # Return the target user requested for demo login
    target_key = target_role or "admin"
    if target_key not in user_instances:
        target_key = "admin"
    return user_instances[target_key]
