from flask import Blueprint, jsonify, make_response , request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.models import Notification , Trek , User , Booking , Review , AuditLog
from controller.extensions import db
from sqlalchemy import func


def create_notification(user_id, message, alert_type="info"):
    new_notif = Notification(user_id=user_id, message=message, type=alert_type)
    db.session.add(new_notif)
    db.session.commit()

def log_system_audit(action, details, severity="info"):
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
    
    # Base query: Only Completed Treks
    query = Trek.query.filter_by(status='Completed')
    
    # RBAC Security Check
    if user.role.name == 'trek_staff':
        # Restrict to ONLY this guide's treks
        if not user.staff_profile:
            return make_response(jsonify({"message": "Staff profile missing."}), 403)
        query = query.filter_by(assigned_staff_id=user.id)
    elif user.role.name != 'admin':
        return make_response(jsonify({"message": "Unauthorized role."}), 403)
        
    completed_treks = query.order_by(Trek.end_date.desc()).all()
    results = []
    
    # Use the aggregation logic we mapped out earlier
    for trek in completed_treks:
        completed_bookings = Booking.query.filter_by(trek_id=trek.trek_id, status='Completed').all()
        cancelled_bookings = Booking.query.filter_by(trek_id=trek.trek_id, status='Cancelled').all()
        
        comp_pax = sum(b.number_of_persons for b in completed_bookings)
        canc_pax = sum(b.number_of_persons for b in cancelled_bookings)
        revenue = sum(b.total_amount for b in completed_bookings if b.payment_status == 'Paid')
        
        reviews = Review.query.filter_by(trek_id=trek.trek_id).all()
        avg_trek = sum(r.trek_rating for r in reviews) / len(reviews) if reviews else 0
        
        # Unique accounts that booked
        unique_accounts = {b.user.id for b in completed_bookings}
        
        # Roster details
        roster = []
        for b in completed_bookings:
            roster.append({
                "name": b.user.name,
                "email": b.user.email,
                "contact": b.user.contact,
                "pax": b.number_of_persons,
                # "medical" : b.instructions 
            })

        avg_staff = sum(r.staff_rating for r in reviews if r.staff_rating) / len([r for r in reviews if r.staff_rating]) if reviews else 0
        
        if trek.assigned_staff_id:
            staff = User.query.get(int(trek.assigned_staff_id))
        
        results.append({
            "trek_id": trek.trek_id,
            "trek_info": {
                "name": trek.trek_name,
                "duration": trek.duration_days,
                "difficulty": trek.difficulty,
                "description": trek.description,
                "location": trek.location,
                "start_date": trek.start_date.strftime("%b %d, %Y"),
                "end_date": trek.end_date.strftime("%b %d, %Y"),
                "altitude": trek.max_altitude,
                "price": trek.price_per_person
            },
            "staff_info": {
                "name": staff.name if staff else "Unassigned",
                "contact": staff.contact if staff else "N/A",
                "email" : staff.email if staff else None,
                "experience": getattr(staff.staff_profile, 'experience_years', "Verified Guide") if staff else "N/A",
                "certification": getattr(staff.staff_profile, 'certification', "ABVIMAS Certified") if staff else "N/A"
            },
            "analytics": {
                "total_revenue": revenue,
                "accounts_booked": len(unique_accounts),
                "completed_participants": comp_pax,
                "cancelled_participants": canc_pax,
                "completion_rate": int((comp_pax / (comp_pax + canc_pax) * 100)) if (comp_pax + canc_pax) > 0 else 0
            },
            "roster": roster,
            "reviews": {
                "trek_avg": round(avg_trek, 1),
                "staff_avg": round(avg_staff, 1),
                "trek_list": [{"id": r.id, "author": r.author.name, "stars": r.trek_rating, "comment": r.trek_experience} for r in reviews if r.trek_rating],
                "staff_list": [{"id": r.id, "author": r.author.name, "stars": r.staff_rating, "comment": r.staff_experience} for r in reviews if r.staff_rating]
            }
        })
        
    return make_response(jsonify(results), 200)