import pytest
from datetime import datetime, timezone, timedelta
from controller.extensions import db
from controller.models import User, Role, Trek, Booking, AuditLog, DispatchTicket
from services.demo_service import is_demo_user, is_demo_target, DEMO_USERS


def get_demo_auth_header(client, role):
    res = client.post("/api/auth/demo-login", json={"role": role})
    assert res.status_code == 200
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestDemoAuthAndReseed:
    def test_demo_login_endpoints_all_roles(self, client):
        # Admin login
        res_admin = client.post("/api/auth/demo-login", json={"role": "admin"})
        assert res_admin.status_code == 200
        data_admin = res_admin.get_json()
        assert data_admin["role"] == "admin"
        assert data_admin["is_demo"] is True
        assert "access_token" in data_admin

        # Staff login
        res_staff = client.post("/api/auth/demo-login", json={"role": "staff"})
        assert res_staff.status_code == 200
        data_staff = res_staff.get_json()
        assert data_staff["role"] == "trek_staff"
        assert data_staff["is_demo"] is True

        # Trekker login
        res_trekker = client.post("/api/auth/demo-login", json={"role": "trekker"})
        assert res_trekker.status_code == 200
        data_trekker = res_trekker.get_json()
        assert data_trekker["role"] == "trekker"
        assert data_trekker["is_demo"] is True

        # Invalid role
        res_invalid = client.post("/api/auth/demo-login", json={"role": "superman"})
        assert res_invalid.status_code == 400

    def test_demo_seeding_creates_required_entities(self, client, app):
        client.post("/api/auth/demo-login", json={"role": "admin"})

        with app.app_context():
            # Check 2 demo staff exist
            staff1 = User.query.filter_by(email="demo.staff1@apex.com").first()
            staff2 = User.query.filter_by(email="demo.staff2@apex.com").first()
            assert staff1 is not None and staff1.role.name == "trek_staff"
            assert staff2 is not None and staff2.role.name == "trek_staff"

            # Check 2 demo trekkers exist
            trekker1 = User.query.filter_by(email="demo.trekker1@apex.com").first()
            trekker2 = User.query.filter_by(email="demo.trekker2@apex.com").first()
            assert trekker1 is not None and trekker1.role.name == "trekker"
            assert trekker2 is not None and trekker2.role.name == "trekker"

            # Check 3 demo treks exist
            demo_treks = Trek.query.filter(Trek.trek_name.like("%(Demo)%")).all()
            assert len(demo_treks) >= 3

            # Check active and completed bookings exist
            bookings = Booking.query.all()
            demo_bookings = [b for b in bookings if is_demo_target(b)]
            statuses = {b.status for b in demo_bookings}
            assert "Confirmed" in statuses or "Active" in statuses or "Booked" in statuses or len(demo_bookings) >= 2

            # Check demo tickets exist
            tickets = DispatchTicket.query.all()
            demo_tickets = [t for t in tickets if is_demo_target(t)]
            assert len(demo_tickets) >= 1

    def test_auto_reseed_self_healing(self, client, app):
        # Initial seed
        client.post("/api/auth/demo-login", json={"role": "admin"})

        with app.app_context():
            # Manually soft-delete or remove one demo trek
            target_trek = Trek.query.filter_by(trek_name="Hampta Pass Expedition (Demo)").first()
            assert target_trek is not None
            target_trek.is_deleted = True
            db.session.commit()

            assert Trek.query.filter_by(trek_name="Hampta Pass Expedition (Demo)", is_deleted=False).first() is None

        # Re-trigger demo login (e.g. user clicks demo button again)
        res = client.post("/api/auth/demo-login", json={"role": "admin"})
        assert res.status_code == 200

        with app.app_context():
            # Verify the demo trek has been automatically restored/undeleted
            restored_trek = Trek.query.filter_by(trek_name="Hampta Pass Expedition (Demo)").first()
            assert restored_trek is not None
            assert restored_trek.is_deleted is False
            assert restored_trek.difficulty == "Moderate"


class TestDemoAdminSimulation:
    def test_admin_cannot_delete_real_trek(self, client, app):
        headers = get_demo_auth_header(client, "admin")
        now = datetime.now(timezone.utc)

        with app.app_context():
            real_trek = Trek(
                trek_name="Real Himalayan High Pass",
                location="Manali, HP",
                price_per_person=12000.0,
                difficulty="Hard",
                available_slots=15,
                duration_days=5,
                start_date=now + timedelta(days=10),
                end_date=now + timedelta(days=15),
                status="Upcoming"
            )
            db.session.add(real_trek)
            db.session.commit()
            real_trek_id = real_trek.trek_id

        # Demo admin tries to delete the real trek
        res = client.delete(f"/api/admin/treks/{real_trek_id}", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is True
        assert "[SIMULATED]" in data.get("message", "")

        # Verify real trek still exists in database and is NOT marked deleted!
        with app.app_context():
            check_trek = Trek.query.get(real_trek_id)
            assert check_trek is not None
            assert check_trek.is_deleted is False

    def test_admin_can_delete_demo_trek(self, client, app):
        headers = get_demo_auth_header(client, "admin")

        with app.app_context():
            demo_trek = Trek.query.filter_by(trek_name="Hampta Pass Expedition (Demo)").first()
            assert demo_trek is not None
            demo_trek_id = demo_trek.trek_id

        res = client.delete(f"/api/admin/treks/{demo_trek_id}", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is not True

        with app.app_context():
            # In Apex, deletion is soft deletion (is_deleted = True)
            deleted_trek = Trek.query.get(demo_trek_id)
            assert deleted_trek.is_deleted is True

    def test_admin_cannot_blacklist_real_user(self, client, app):
        headers = get_demo_auth_header(client, "admin")

        with app.app_context():
            real_user = User.query.filter_by(email="trekker@test.com").first()
            assert real_user is not None
            assert real_user.is_active is True
            user_id = real_user.id

        # Demo admin attempts to toggle status of real user
        res = client.patch(f"/api/admin/users/{user_id}/toggle-status", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is True

        # Verify real user is still active in database
        with app.app_context():
            check_user = User.query.get(user_id)
            assert check_user.is_active is True

    def test_admin_create_staff_is_simulated(self, client, app):
        headers = get_demo_auth_header(client, "admin")

        new_staff_payload = {
            "name": "Simulated Staff Candidate",
            "email": "candidate@example.com",
            "password": "TemporaryPassword123!",
            "contact": "9876543299",
            "specialization": "Rock Climbing",
            "experience_years": 4,
            "certification": "Basic Mountaineering"
        }
        res = client.post("/api/admin/staff", json=new_staff_payload, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data.get("simulated") is True

        # Verify candidate was not actually written to database
        with app.app_context():
            assert User.query.filter_by(email="candidate@example.com").first() is None

    def test_admin_cannot_wipe_real_audit_logs(self, client, app):
        headers = get_demo_auth_header(client, "admin")

        with app.app_context():
            log = AuditLog(
                action="REAL_SYSTEM_CONFIG_UPDATE",
                details="Crucial live configuration updated",
                severity="info"
            )
            db.session.add(log)
            db.session.commit()
            log_id = log.id

        res = client.delete("/api/admin/profile/audit-logs", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is True

        # Verify real audit log was preserved!
        with app.app_context():
            assert AuditLog.query.get(log_id) is not None


class TestDemoTrekkerAndStaffSimulation:
    def test_demo_trekker_cannot_delete_profile(self, client, app):
        headers = get_demo_auth_header(client, "trekker")

        res = client.delete("/api/trekker/profile", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is True

        # Verify demo trekker profile still exists
        with app.app_context():
            assert User.query.filter_by(email="demo.trekker1@apex.com").first() is not None

    def test_demo_staff_cannot_mutate_real_trek(self, client, app):
        headers = get_demo_auth_header(client, "staff")
        now = datetime.now(timezone.utc)

        with app.app_context():
            demo_staff = User.query.filter_by(email="demo.staff1@apex.com").first()
            assert demo_staff is not None

            real_trek = Trek(
                trek_name="Protected High Altitude Route",
                location="Kullu, HP",
                price_per_person=9000.0,
                difficulty="Easy",
                available_slots=10,
                duration_days=3,
                assigned_staff_id=demo_staff.id,
                start_date=now + timedelta(days=10),
                end_date=now + timedelta(days=13),
                status="Upcoming"
            )
            db.session.add(real_trek)
            db.session.commit()
            trek_id = real_trek.trek_id

        update_payload = {
            "status": "Completed",
            "field_report": "Finished expedition smoothly"
        }
        res = client.patch(f"/api/trek_staff/treks/{trek_id}/update-field-data", json=update_payload, headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data.get("simulated") is True

        with app.app_context():
            check_trek = Trek.query.get(trek_id)
            # Real trek status remains unchanged
            assert check_trek.status == "Upcoming"

    def test_demo_user_actions_do_not_pollute_audit_log(self, client, app):
        headers = get_demo_auth_header(client, "admin")

        # Initial audit log count
        with app.app_context():
            initial_count = AuditLog.query.count()

        # Demo admin executes simulated action
        client.delete("/api/admin/profile/audit-logs", headers=headers)

        with app.app_context():
            new_count = AuditLog.query.count()
            # Count must NOT have increased with a demo user audit entry
            assert new_count == initial_count
