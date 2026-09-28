import pytest
from datetime import datetime, timezone, timedelta
from controller.extensions import db
from controller.models import User, Role, Trek, Booking, AuditLog, DispatchTicket, StaffProfile
from services.demo_service import is_demo_user, is_demo_target


def get_demo_auth_header(client, role):
    res = client.post("/api/auth/demo-login", json={"role": role})
    assert res.status_code == 200
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestMilestone3SafeSimulation:
    def test_admin_trek_update_simulation(self, client, app):
        """Verify demo admin cannot mutate a real operational expedition route."""
        headers = get_demo_auth_header(client, "admin")
        now = datetime.now(timezone.utc)

        with app.app_context():
            real_trek = Trek(
                trek_name="Everest Base Camp Live",
                location="Khumbu, Nepal",
                price_per_person=25000.0,
                difficulty="Hard",
                available_slots=12,
                duration_days=14,
                start_date=now + timedelta(days=30),
                end_date=now + timedelta(days=44),
                status="Open"
            )
            db.session.add(real_trek)
            db.session.commit()
            real_trek_id = real_trek.trek_id

        update_payload = {
            "trek_name": "Tampered Route Name",
            "status": "Cancelled",
            "cancellation_reason": "Simulated abort"
        }
        res = client.put(f"/api/admin/treks/{real_trek_id}", json=update_payload, headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is True
        assert "[SIMULATED]" in data.get("message", "")

        # Verify real database record was preserved
        with app.app_context():
            check_trek = Trek.query.get(real_trek_id)
            assert check_trek.trek_name == "Everest Base Camp Live"
            assert check_trek.status == "Open"

    def test_admin_trek_update_on_demo_target(self, client, app):
        """Verify demo admin can edit a (Demo)-tagged trek."""
        headers = get_demo_auth_header(client, "admin")

        with app.app_context():
            demo_trek = Trek.query.filter_by(trek_name="Rohtang Valley Trail (Demo)").first()
            assert demo_trek is not None
            demo_trek_id = demo_trek.trek_id

        update_payload = {
            "trek_name": "Rohtang Valley Trail (Demo)",
            "location": "Updated Kullu Valley, HP",
            "difficulty": "Easy",
            "duration_days": 4,
            "available_slots": 14,
            "description": "Updated trail notes",
            "max_altitude": 4000.0,
            "price_per_person": 5000.0
        }
        res = client.put(f"/api/admin/treks/{demo_trek_id}", json=update_payload, headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is not True

        with app.app_context():
            check_trek = Trek.query.get(demo_trek_id)
            assert check_trek.duration_days == 4
            assert check_trek.price_per_person == 5000.0

    def test_admin_staff_override_simulation(self, client, app):
        """Verify demo admin cannot alter real guide assignments on real routes."""
        headers = get_demo_auth_header(client, "admin")
        now = datetime.now(timezone.utc)

        with app.app_context():
            real_staff = User.query.filter_by(email="staff@test.com").first()
            assert real_staff is not None
            real_staff_id = real_staff.id

            real_trek = Trek(
                trek_name="Real Kedarkantha Summit",
                location="Uttarakhand",
                price_per_person=8000.0,
                difficulty="Easy",
                available_slots=20,
                duration_days=4,
                start_date=now + timedelta(days=20),
                end_date=now + timedelta(days=24),
                status="Open"
            )
            db.session.add(real_trek)
            db.session.commit()
            real_trek_id = real_trek.trek_id

        override_payload = {
            "trek_id": real_trek_id,
            "staff_id": real_staff_id,
            "force_switch": True
        }
        res = client.patch("/api/admin/assign-staff-override", json=override_payload, headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is True
        assert "[SIMULATED]" in data.get("message", "")

        # Verify assigned_staff_id on real trek is still unchanged (None)
        with app.app_context():
            check_trek = Trek.query.get(real_trek_id)
            assert check_trek.assigned_staff_id is None

    def test_admin_ticket_resolve_simulation(self, client, app):
        """Verify demo admin cannot resolve or alter real user dispatch tickets."""
        headers = get_demo_auth_header(client, "admin")

        with app.app_context():
            real_user = User.query.filter_by(email="trekker@test.com").first()
            assert real_user is not None

            real_ticket = DispatchTicket(
                author_id=real_user.id,
                subject="Real Expedition Hazard Alert",
                message="Rockfall reported near ridge sector 4.",
                priority="Hazard",
                status="Pending"
            )
            db.session.add(real_ticket)
            db.session.commit()
            real_ticket_id = real_ticket.id

        resolve_payload = {
            "response": "Simulated resolution text by demo admin."
        }
        res = client.patch(f"/api/admin/tickets/{real_ticket_id}/resolve", json=resolve_payload, headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is True
        assert "[SIMULATED]" in data.get("message", "")

        # Verify real ticket remains in Pending status with no response
        with app.app_context():
            check_ticket = DispatchTicket.query.get(real_ticket_id)
            assert check_ticket.status == "Pending"
            assert check_ticket.admin_response is None

    def test_trekker_booking_simulation(self, client, app):
        """Verify demo trekker booking real trek does not deplete real slots."""
        headers = get_demo_auth_header(client, "trekker")
        now = datetime.now(timezone.utc)

        with app.app_context():
            real_trek = Trek(
                trek_name="Real Markha Valley Trek",
                location="Ladakh",
                price_per_person=18000.0,
                difficulty="Moderate",
                available_slots=10,
                duration_days=6,
                start_date=now + timedelta(days=40),
                end_date=now + timedelta(days=46),
                status="Open"
            )
            db.session.add(real_trek)
            db.session.commit()
            real_trek_id = real_trek.trek_id

        booking_payload = {
            "trek_id": real_trek_id,
            "adults": 2,
            "children": 0,
            "seniors": 0,
            "payment_method": "Credit Card",
            "medical_instructions": "None"
        }
        res = client.post("/api/trekker/bookings", json=booking_payload, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data.get("simulated") is True
        assert "[SIMULATED]" in data.get("message", "")

        # Verify real slots were NOT decremented
        with app.app_context():
            check_trek = Trek.query.get(real_trek_id)
            assert check_trek.available_slots == 10


class TestMilestone3RoleSwitchFlow:
    def test_seamless_role_switch_across_all_roles(self, client):
        """Test transitioning between Admin, Staff, and Trekker demo sessions."""
        # 1. Start as Admin
        res_admin = client.post("/api/auth/demo-login", json={"role": "admin"})
        assert res_admin.status_code == 200
        admin_data = res_admin.get_json()
        assert admin_data["role"] == "admin"
        assert admin_data["is_demo"] is True

        # 2. Switch to Staff Guide
        res_staff = client.post("/api/auth/demo-login", json={"role": "trek_staff"})
        assert res_staff.status_code == 200
        staff_data = res_staff.get_json()
        assert staff_data["role"] == "trek_staff"
        assert staff_data["is_demo"] is True

        # 3. Switch to Trekker
        res_trekker = client.post("/api/auth/demo-login", json={"role": "trekker"})
        assert res_trekker.status_code == 200
        trekker_data = res_trekker.get_json()
        assert trekker_data["role"] == "trekker"
        assert trekker_data["is_demo"] is True

        # 4. Switch back to Admin
        res_admin_return = client.post("/api/auth/demo-login", json={"role": "admin"})
        assert res_admin_return.status_code == 200
        return_data = res_admin_return.get_json()
        assert return_data["role"] == "admin"
        assert return_data["is_demo"] is True
