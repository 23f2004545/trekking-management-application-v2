from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.models import Notification
from controller.extensions import db


def create_notification(user_id, message, alert_type="info"):
    new_notif = Notification(user_id=user_id, message=message, type=alert_type)
    db.session.add(new_notif)
    db.session.commit()


utils_bp = Blueprint('utils', __name__)

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