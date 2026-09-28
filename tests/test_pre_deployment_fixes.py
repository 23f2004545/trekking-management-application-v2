import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from controller.models import User, Trek, Role, StaffProfile, db
from services.demo_service import seed_or_reset_demo_data, is_demo_user


def get_demo_auth_header(client, role):
    res = client.post("/api/auth/demo-login", json={"role": role})
    assert res.status_code == 200
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestPreDeploymentFixes:
    def test_demo_trek_staff_assignment_integrity(self, client, app):
        """Verify seeded demo treks have assigned_staff_id pointing to genuine trek_staff, not Admin."""
        with app.app_context():
            seed_or_reset_demo_data()
            admin_user = User.query.filter_by(email="demo.admin@apex.com").first()
            demo_treks = Trek.query.filter(Trek.trek_name.like("%(Demo)%")).all()
            assert len(demo_treks) >= 3

            for trek in demo_treks:
                assert trek.assigned_staff_id is not None
                assert trek.assigned_staff_id != admin_user.id
                guide = User.query.get(trek.assigned_staff_id)
                assert guide is not None
                assert guide.role.name == "trek_staff"
                assert "staff" in guide.email

    def test_demo_admin_trek_creation_simulation(self, client, app):
        """Verify demo admin creating a trek receives simulated 201 without persisting to DB."""
        headers = get_demo_auth_header(client, "admin")
        initial_count = 0
        with app.app_context():
            initial_count = Trek.query.count()

        payload = {
            "name": "Simulated Alpine Trail",
            "location": "Kullu Valley",
            "difficulty": "Easy",
            "duration": 3,
            "available_slots": 10,
            "start_date": "2026-10-15",
            "end_date": "2026-10-18",
            "max_altitude": 3200,
            "price_per_person": 5000,
            "description": "Simulation trail for demo testing"
        }

        res = client.post("/api/admin/treks", data=payload, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data.get("simulated") is True
        assert "[SIMULATED]" in data.get("message", "")

        with app.app_context():
            final_count = Trek.query.count()
            assert final_count == initial_count
            created = Trek.query.filter_by(trek_name="Simulated Alpine Trail").first()
            assert created is None

    def test_purge_trek_soft_deletes_record(self, client, app):
        """Verify purging a trek sets is_deleted = True and handles staff lookup cleanly."""
        headers = None
        trek_id = None
        with app.app_context():
            # Create a real admin user and a real trek with string/int assigned_staff_id
            admin_role = Role.query.filter_by(name="admin").first()
            staff_role = Role.query.filter_by(name="trek_staff").first()

            staff_user = User.query.filter_by(email="real_staff_purge_test@apex.com").first()
            if not staff_user:
                staff_user = User(
                    name="Real Purge Guide",
                    email="real_staff_purge_test@apex.com",
                    password="TestPassword123!",
                    contact="9999991111",
                    role=staff_role,
                    is_active=True
                )
                db.session.add(staff_user)
                db.session.flush()

            real_admin = User.query.filter_by(email="real_admin_purge_test@apex.com").first()
            if not real_admin:
                real_admin = User(
                    name="Real Admin Purge",
                    email="real_admin_purge_test@apex.com",
                    password="TestPassword123!",
                    contact="9999992222",
                    role=admin_role,
                    is_active=True
                )
                db.session.add(real_admin)
                db.session.flush()

            real_trek = Trek(
                trek_name="Purge Verification Route",
                location="Uttarakhand",
                difficulty="Moderate",
                duration_days=4,
                available_slots=15,
                start_date=datetime.now(timezone.utc).date() + timedelta(days=10),
                end_date=datetime.now(timezone.utc).date() + timedelta(days=14),
                price_per_person=6000.0,
                max_altitude=3800.0,
                assigned_staff_id=staff_user.id,
                is_deleted=False
            )
            db.session.add(real_trek)
            db.session.commit()
            trek_id = real_trek.trek_id

            from flask_jwt_extended import create_access_token
            token = create_access_token(identity=str(real_admin.id))
            headers = {"Authorization": f"Bearer {token}"}

        # Purge the trek via API
        res = client.delete(f"/api/admin/treks/{trek_id}", headers=headers)
        assert res.status_code == 200
        assert "removed successfully" in res.get_json()["message"]

        with app.app_context():
            purged = Trek.query.get(trek_id)
            assert purged is not None
            assert purged.is_deleted is True

    def test_export_history_telemetry_demo_email_propagation(self, client, app):
        """Verify export historical telemetry endpoint propagates demo_delivery_email."""
        headers = get_demo_auth_header(client, "admin")

        with patch("tasks.export_history_telemetry.delay") as mock_delay:
            mock_delay.return_value = None
            payload = {
                "trek_info": {
                    "name": "Hampta Pass Expedition (Demo)",
                    "duration": 5,
                    "altitude": 4270,
                    "start_date": "2026-10-01",
                    "end_date": "2026-10-06"
                },
                "analytics": {"total_revenue": 75000},
                "staff_info": {"name": "Tenzing Norgay", "email": "demo.staff1@apex.com"},
                "demo_delivery_email": "evaluator.preview@example.com"
            }

            res = client.post("/api/utils/export-history", json=payload, headers=headers)
            assert res.status_code == 200
            assert mock_delay.called

            _, kwargs = mock_delay.call_args
            assert kwargs.get("demo_delivery_email") == "evaluator.preview@example.com"
