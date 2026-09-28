from flask import Blueprint, jsonify, make_response , request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.models import Notification , Trek , User , Booking , Review , AuditLog , DispatchTicket
from controller.extensions import db
from sqlalchemy import func


def create_notification(user_id, message, alert_type="info"):
    new_notif = Notification(user_id=user_id, message=message, type=alert_type)
    db.session.add(new_notif)
    db.session.commit()

def log_system_audit(action, details, severity="info"):
    try:
        from flask_jwt_extended import get_jwt_identity
        from services.demo_service import is_demo_user
        user_id = get_jwt_identity()
        if user_id:
            user = User.query.get(int(user_id))
            if is_demo_user(user):
                # Demo actions are simulated and do not pollute the operational audit log
                return
    except Exception:
        pass

    new_log = AuditLog(action=action, details=details, severity=severity)
    db.session.add(new_log)
    db.session.commit()

utils_bp = Blueprint('utils', __name__)


@utils_bp.route('/trek-extremes', methods=['GET'])
def get_trek_extremes():
    
    status_filter = request.args.get('status')
    
    query = Trek.query
    if status_filter:
        # If Trekker requests it, only looking at Open/Ongoing treks
        query = query.filter(Trek.status=='Open')
        
    max_price = db.session.query(db.func.max(query.subquery().c.price_per_person)).scalar() or 10000
    min_price = db.session.query(db.func.min(query.subquery().c.price_per_person)).scalar() or 0
    max_alt = db.session.query(db.func.max(query.subquery().c.max_altitude)).scalar() or 5000
    min_alt = db.session.query(db.func.min(query.subquery().c.max_altitude)).scalar() or 0
        
    return jsonify({
        "max_price": int(max_price),
        "min_price": int(min_price),
        "max_altitude": int(max_alt),
        "min_altitude": int(min_alt)
    }), 200
    

@utils_bp.route('/public/landing-data', methods=['GET'])
def get_landing_data():
    # ==========================================
    # 1. THE 4 CORE METRICS
    # ==========================================
    # Highest Peak Reached (Max altitude of all treks)
    highest_peak = db.session.query(func.max(Trek.max_altitude)).scalar() or 0
    
    # Active Staff Count
    total_staff = User.query.filter(User.role.has(name='trek_staff')).count()
    
    # Successfully Handled Participants (Sum of persons in 'Completed' bookings)
    successful_participants = db.session.query(func.sum(Booking.number_of_persons)).filter(
        Trek.status == 'Completed'
    ).scalar() or 0
    
    # Treks Deployed (Count of 'Completed' treks)
    treks_deployed = Trek.query.filter_by(status='Completed').count()

    # ==========================================
    # 2. SOCIAL PROOF (REVIEWS)
    # ==========================================
    # Overall Average Trek Rating
    avg_rating_raw = db.session.query(func.avg(Review.trek_rating)).scalar()
    avg_rating = round(avg_rating_raw, 1) if avg_rating_raw else 4.8 # Fallback if completely empty
    
    # Latest 10 Reviews
    real_reviews_query = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    real_reviews = [{
        "author": r.author.name,
        "rating": r.trek_rating,
        "comment": r.trek_experience
    } for r in real_reviews_query]

    # ==========================================
    # 3. FOMO ENGINE DATA (Active Treks)
    # ==========================================
    # Fetch names of treks currently accepting bookings
    active_treks_query = Trek.query.filter(Trek.status.in_(['Open', 'Ongoing'])).limit(10).all()
    active_treks = [t.trek_name for t in active_treks_query]
    
    # Fallback just in case database is brand new
    if not active_treks:
        active_treks = ["Rohtang Pass", "Kheerganga Ridge", "Bhrigu Lake Circuit", "Hampta Pass Corridor"]

    return make_response(jsonify({
        "metrics": {
            "highest_peak": int(highest_peak),
            "total_staff": total_staff,
            "successful_participants": int(successful_participants),
            "treks_deployed": treks_deployed
        },
        "reviews": {
            "average": avg_rating,
            "list": real_reviews
        },
        "fomo_treks": active_treks
    }), 200)


@utils_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_my_notifications():
    user_id = get_jwt_identity()
    notifs = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(20).all()
    
    return make_response(jsonify([{
        "id": n.id,
        "message": n.message,
        "type": n.type,
        "is_read": n.is_read,
        "created_at": n.created_at.strftime("%b %d, %H:%M")
    } for n in notifs]), 200)

@utils_bp.route('/notifications/<int:notif_id>/read', methods=['PATCH'])
@jwt_required()
def mark_read(notif_id):
    notif = Notification.query.filter_by(id=notif_id, user_id=get_jwt_identity()).first_or_404()
    notif.is_read = True
    db.session.commit()
    return make_response(jsonify({"message": "Marked read"}), 200)

@utils_bp.route('/notifications/<int:notif_id>', methods=['DELETE'])
@jwt_required()
def delete_notif(notif_id):
    notif = Notification.query.filter_by(id=notif_id, user_id=get_jwt_identity()).first_or_404()
    db.session.delete(notif)
    db.session.commit()
    return make_response(jsonify({"message": "Deleted"}), 200)

@utils_bp.route('/notifications/clear', methods=['DELETE'])
@jwt_required()
def clear_all():
    Notification.query.filter_by(user_id=get_jwt_identity()).delete()
    db.session.commit()
    return make_response(jsonify({"message": "All cleared"}), 200)


@utils_bp.route('/history', methods=['GET'])
@jwt_required()
def get_historical_treks():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    is_onboarded = True
    if user.role.name == 'trek_staff':
        if not user.staff_profile:
            return make_response(jsonify({"message": "Staff profile missing."}), 403)
        is_onboarded = user.staff_profile.emergency_contact != "1234567890"

    # 1. Fetch all archived bookings (Completed or Cancelled)
    past_bookings_query = Booking.query.filter(Booking.status.in_(['Completed', 'Cancelled']))
    
    if user.role.name == 'trek_staff':
        past_bookings_query = past_bookings_query.join(Trek).filter(Trek.assigned_staff_id == user.id)
    elif user.role.name != 'admin':
        return make_response(jsonify({"message": "Unauthorized role clearance."}), 403)
        
    all_past_bookings = past_bookings_query.all()

    # 2. GROUPING ENGINE: Map bookings into unique Departure Cohorts
    # Key format: "trekId_YYYY-MM-DD"
    cohorts = {}

    for b in all_past_bookings:
        t = b.trek
        # Pull from your new snapshots, fallback to Trek table if testing older un-migrated rows
        s_start = getattr(b, 'snapshot_start_date', None) or t.start_date
        s_end = getattr(b, 'snapshot_end_date', None) or t.end_date
        s_price = getattr(b, 'snapshot_price', None) or t.price_per_person
        
        start_str = s_start.strftime("%Y-%m-%d") if hasattr(s_start, 'strftime') else str(s_start)
        cohort_key = f"{t.trek_id}_{start_str}"

        if cohort_key not in cohorts:
            cohorts[cohort_key] = {
                "trek": t,
                "start_date": s_start,
                "end_date": s_end,
                "price": s_price,
                "completed": [],
                "cancelled": []
            }
            
        if b.status == 'Completed': cohorts[cohort_key]["completed"].append(b)
        elif b.status == 'Cancelled': cohorts[cohort_key]["cancelled"].append(b)

    # 3. Secondary Failsafe: Catch completed treks that had 0 bookings
    empty_treks = Trek.query.filter_by(status='Completed').all()
    if user.role.name == 'trek_staff':
        empty_treks = [t for t in empty_treks if t.assigned_staff_id == user.id]

    for t in empty_treks:
        start_str = t.start_date.strftime("%Y-%m-%d") if hasattr(t.start_date, 'strftime') else str(t.start_date)
        key = f"{t.trek_id}_{start_str}"
        if key not in cohorts:
            cohorts[key] = {"trek": t, "start_date": t.start_date, "end_date": t.end_date, "price": t.price_per_person, "completed": [], "cancelled": []}

    # 4. Compile final payload matching your exact UI dictionary
    results = []
    
    for key, data in cohorts.items():
        t = data["trek"]
        comp_b = data["completed"]
        canc_b = data["cancelled"]

        comp_pax = sum(b.number_of_persons for b in comp_b)
        canc_pax = sum(b.number_of_persons for b in canc_b)
        
        revenue = sum(
            (getattr(b, 'snapshot_price', data["price"]) * b.number_of_persons) 
            for b in comp_b if getattr(b, 'payment_status', 'Paid') == 'Paid'
        )
        
        unique_accounts = {b.user.id for b in comp_b if b.user}
        
        roster = [{
            "name": b.user.name, "email": b.user.email, "contact": b.user.contact,
            "pax": b.number_of_persons, 
            "medical": getattr(b, 'medical_instructions', getattr(b, 'instructions', 'Clear. No conditions flagged.'))
        } for b in comp_b if b.user]

        reviews = Review.query.filter_by(trek_id=t.trek_id).all()
        avg_trek = sum(r.trek_rating for r in reviews) / len(reviews) if reviews else 0
        avg_staff = sum(r.staff_rating for r in reviews if r.staff_rating) / len([r for r in reviews if r.staff_rating]) if reviews else 0
        
        staff_id_val = getattr(t, 'assigned_staff_id', None)
        staff = User.query.get(int(staff_id_val)) if (staff_id_val and str(staff_id_val).isdigit()) else None

        fmt_s = data["start_date"].strftime("%b %d, %Y") if hasattr(data["start_date"], 'strftime') else str(data["start_date"])
        fmt_e = data["end_date"].strftime("%b %d, %Y") if hasattr(data["end_date"], 'strftime') else str(data["end_date"])

        results.append({
            "trek_id": t.trek_id,
            "cancellation_date" : t.cancelled_at.strftime("%b %d, %Y") if t.status == 'Cancelled' else None,
            "cancellation_reason" : t.cancellation_reason if t.status == 'Cancelled' else None,
            "trek_info": {
                "name": t.trek_name, "duration": t.duration_days, "difficulty": t.difficulty,
                "description": t.description or "An immersive high-altitude wilderness expedition traversing ancient alpine meadows and glacial networks.",
                "location": t.location, "start_date": fmt_s, "end_date": fmt_e,
                "altitude": t.max_altitude, "price": data["price"],
                "status" : t.status 
            },
            "staff_info": {
                "name": staff.name if staff else "Unassigned",
                "contact": staff.contact if staff else "N/A",
                "email": staff.email if staff else "None",
                "experience": getattr(staff.staff_profile, 'experience_years', "Verified") if (staff and hasattr(staff, 'staff_profile')) else "N/A",
                "certification": getattr(staff.staff_profile, 'certification', "ABVIMAS Cleared") if (staff and hasattr(staff, 'staff_profile')) else "N/A",
                "profile_pic" : staff.profile_pic if staff else "/static/Profile_pics/trek_staff.png"
            },
            "analytics": {
                "total_revenue": revenue, "accounts_booked": len(unique_accounts),
                "completed_participants": comp_pax, "cancelled_participants": canc_pax,
                "completion_rate": int((comp_pax / (comp_pax + canc_pax) * 100)) if (comp_pax + canc_pax) > 0 else 100
            },
            "roster": roster,
            "reviews": {
                "trek_avg": round(avg_trek, 1), "staff_avg": round(avg_staff, 1),
                "trek_list": [{"id": r.id, "author": r.author.name, "stars": r.trek_rating, "comment": r.trek_experience} for r in reviews if r.trek_rating],
                "staff_list": [{"id": r.id, "author": r.author.name, "stars": r.staff_rating, "comment": r.staff_experience} for r in reviews if r.staff_rating]
            }
        })

    # Sort most recently completed trip first
    results.sort(key=lambda x: x["trek_info"]["end_date"], reverse=True)
    return make_response(jsonify({"is_onboarded": is_onboarded, "results": results}), 200)


@utils_bp.route('/export-history', methods=['POST'])
@jwt_required()
def export_historical_data():
    from tasks import export_history_telemetry
    from services.demo_service import is_demo_user
    
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    payload = request.get_json() or {}
    
    # Extract demo email if running in demo profile mode
    demo_delivery_email = payload.get('demo_delivery_email') if is_demo_user(user) else None
    
    # Fire the Celery worker asynchronously
    export_history_telemetry.delay(user.email, user.name, payload, demo_delivery_email=demo_delivery_email)
    
    return jsonify({"message": "Telemetry export initialized. Check your encrypted inbox."}), 200


@utils_bp.route('/tickets', methods=['POST', 'GET'])
@jwt_required()
def handle_my_tickets():
    user_id = get_jwt_identity()
    
    if request.method == 'POST':
        # Prevent spam: Check if they already have a Pending ticket
        existing = DispatchTicket.query.filter_by(author_id=user_id, status='Pending').first()
        if existing:
            return make_response(jsonify({"message": "You already have an active dispatch in queue."}), 400)

        data = request.get_json()
        new_ticket = DispatchTicket(
            author_id=user_id,
            subject=data.get('subject'),
            message=data.get('message'),
            priority=data.get('priority', 'Routine')
        )
        db.session.add(new_ticket)
        db.session.commit()
        return make_response(jsonify({"message": "Dispatch ticket transmitted to Central Command."}), 201)
        
    if request.method == 'GET':
        # Return only their active pending ticket (if any)
        active_ticket = DispatchTicket.query.filter_by(author_id=user_id, status='Pending').first()
        if not active_ticket:
            return make_response(jsonify(None), 200)
            
        return make_response(jsonify({
            "id": active_ticket.id, 
            "subject": active_ticket.subject, 
            "message": active_ticket.message, 
            "priority": active_ticket.priority,
            "status": active_ticket.status, 
            "date": active_ticket.created_at.strftime("%b %d, %H:%M")
        }), 200)

@utils_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
@jwt_required()
def withdraw_ticket(ticket_id):
    user_id = get_jwt_identity()
    ticket = DispatchTicket.query.filter_by(id=ticket_id, author_id=user_id).first_or_404()
    
    db.session.delete(ticket)
    db.session.commit()
    return make_response(jsonify({"message": "Dispatch ticket successfully withdrawn."}), 200)