from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.models import Notification , Trek , User , Booking , Review
from controller.extensions import db
from sqlalchemy import func


def create_notification(user_id, message, alert_type="info"):
    new_notif = Notification(user_id=user_id, message=message, type=alert_type)
    db.session.add(new_notif)
    db.session.commit()


utils_bp = Blueprint('utils', __name__)


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

