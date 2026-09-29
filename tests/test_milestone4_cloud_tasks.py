import os
import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from controller.extensions import db, cache
from controller.models import User, Role
from config import config
from mail import send_html_email
import tasks

@pytest.fixture(scope='module')
def app_instance():
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['CACHE_TYPE'] = 'SimpleCache'
    os.environ['CELERY_TASK_ALWAYS_EAGER'] = 'True'

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'CACHE_TYPE': 'SimpleCache',
        'CELERY_TASK_ALWAYS_EAGER': True
    })

    # Re-initialize cache with SimpleCache for in-memory testing without external Redis socket
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})

    with app.app_context():
        db.create_all()
        admin_role = Role(name='admin')
        staff_role = Role(name='trek_staff')
        trekker_role = Role(name='trekker')
        db.session.add_all([admin_role, staff_role, trekker_role])
        db.session.commit()

        # Seed sample users
        admin_user = User(
            name="Apex Administrator",
            email="admin@apex.com",
            password="hashed_admin_pass",
            role=admin_role,
            contact="1111111111"
        )
        real_user = User(
            name="John Explorer",
            email="john@realuser.com",
            password="hashed_john_pass",
            role=trekker_role,
            contact="2222222222"
        )
        demo_trekker = User(
            name="Demo Explorer One",
            email="trekker@demo.apex.com",
            password="hashed_demo_pass",
            role=trekker_role,
            contact="3333333333"
        )
        db.session.add_all([admin_user, real_user, demo_trekker])
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()


class TestCeleryAndRedisConfig:
    def test_broker_url_default_fallback(self):
        """Verifies default Celery broker url and eager fallback."""
        assert config.CELERY_BROKER_URL is not None
        assert isinstance(config.CELERY_TASK_ALWAYS_EAGER, bool)

    def test_tasks_celery_configuration(self):
        """Verifies Celery app has proper timezone and broker configured."""
        assert tasks.celery_app.conf.timezone == 'Asia/Kolkata'
        assert tasks.celery_app.conf.broker_url is not None


class TestSMTPFallbackAndDispatch:
    def test_send_html_email_safe_console_fallback_without_creds(self, monkeypatch):
        """When SMTP credentials are missing, send_html_email should log safely without raising."""
        monkeypatch.setattr(config, 'SMTP_USER', '')
        monkeypatch.setattr(config, 'SMTP_PASSWORD', '')

        # Should safely return True (gracefully handled) and not throw an exception
        result = send_html_email('visitor@example.com', 'Test Subject', '<h1>Test</h1>')
        assert result is True

    @patch('mail.smtplib.SMTP')
    def test_send_html_email_with_mocked_smtp_tls(self, mock_smtp_cls, monkeypatch):
        """When SMTP credentials are provided, send_html_email connects and sends via TLS."""
        monkeypatch.setattr(config, 'SMTP_HOST', 'smtp-relay.brevo.com')
        monkeypatch.setattr(config, 'SMTP_PORT', 587)
        monkeypatch.setattr(config, 'SMTP_USER', 'apikey')
        monkeypatch.setattr(config, 'SMTP_PASSWORD', 'supersecret')
        monkeypatch.setattr(config, 'SMTP_USE_TLS', True)
        monkeypatch.setattr(config, 'SMTP_USE_SSL', False)
        monkeypatch.setattr(config, 'SMTP_SENDER_EMAIL', 'noreply@apex.com')
        monkeypatch.setattr(config, 'SMTP_SENDER_NAME', 'Apex Support')

        mock_server = MagicMock()
        mock_smtp_cls.return_value.__enter__.return_value = mock_server

        result = send_html_email('visitor@example.com', 'Welcome Expedition', '<p>Details</p>')
        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('apikey', 'supersecret')
        mock_server.send_message.assert_called_once()


class TestDemoDeliveryEmailRouting:
    @patch('tasks.send_brevo_email')
    def test_export_history_csv_routes_to_demo_delivery_email(self, mock_send, app_instance):
        """If demo_delivery_email is specified, export_history_csv routes to it."""
        with app_instance.app_context():
            user = User.query.filter_by(email="trekker@demo.apex.com").first()
            tasks.export_history_csv(user.id, user.email, user.name, demo_delivery_email="visitor@portfolio.com")

            mock_send.assert_called_once()
            called_args = mock_send.call_args[0]
            assert called_args[0] == "visitor@portfolio.com"
            assert "Your Expedition History CSV is Ready" in called_args[2]
            assert "DEMO PREVIEW" in called_args[3]

    @patch('tasks.send_brevo_email')
    def test_export_history_csv_routes_to_real_user_email_when_none(self, mock_send, app_instance):
        """For real registered users, delivery email remains strictly their DB email."""
        with app_instance.app_context():
            user = User.query.filter_by(email="john@realuser.com").first()
            tasks.export_history_csv(user.id, user.email, user.name, demo_delivery_email=None)

            mock_send.assert_called_once()
            called_args = mock_send.call_args[0]
            assert called_args[0] == "john@realuser.com"
            assert "DEMO PREVIEW" not in called_args[3]

    @patch('tasks.send_brevo_email')
    def test_send_otp_email_demo_delivery(self, mock_send):
        """send_otp_email routes to demo_delivery_email if provided."""
        tasks.send_otp_email("trekker@demo.apex.com", "Demo User", "123456", demo_delivery_email="visitor@portfolio.com")
        mock_send.assert_called_once()
        called_args = mock_send.call_args[0]
        assert called_args[0] == "visitor@portfolio.com"
        assert "123456" in called_args[3]
        assert "DEMO PREVIEW" in called_args[3]

    @patch('tasks.send_brevo_email')
    def test_send_staff_credentials_email_demo_delivery(self, mock_send, app_instance):
        """send_staff_credentials_email routes to demo_delivery_email if provided."""
        with app_instance.app_context():
            tasks.send_staff_credentials_email(
                "candidate@test.com", "staff_new@apex.com", "TempPass123",
                demo_delivery_email="visitor@portfolio.com"
            )
            mock_send.assert_called_once()
            called_args = mock_send.call_args[0]
            assert called_args[0] == "visitor@portfolio.com"
            assert "staff_new@apex.com" in called_args[3]
            assert "DEMO PREVIEW" in called_args[3]

    @patch('tasks.send_brevo_email')
    def test_dispatch_ticket_resolution_demo_delivery(self, mock_send):
        """dispatch_ticket_resolution routes to demo_delivery_email if provided."""
        tasks.dispatch_ticket_resolution(
            "author@demo.apex.com", "Explorer Demo", "trekker",
            "Trail Question", "Where is checkpoint B?", "It is at mile 4.",
            demo_delivery_email="visitor@portfolio.com"
        )
        mock_send.assert_called_once()
        called_args = mock_send.call_args[0]
        assert called_args[0] == "visitor@portfolio.com"
        assert "Where is checkpoint B?" in called_args[3]
        assert "DEMO PREVIEW" in called_args[3]


class TestEndpointDemoDeliveryPropagation:
    @patch('routes.auth_apis.cache.set')
    @patch('routes.auth_apis.send_otp_email.delay')
    def test_auth_request_otp_demo_delivery_propagation(self, mock_delay, mock_cache, app_instance):
        """POST /api/auth/request-login-otp forwards demo_delivery_email when requested by demo user."""
        client = app_instance.test_client()
        res = client.post('/api/auth/request-login-otp', json={
            'email': 'trekker@demo.apex.com',
            'demo_delivery_email': 'visitor@portfolio.com'
        })
        assert res.status_code == 200
        mock_delay.assert_called_once()
        kwargs = mock_delay.call_args[1]
        assert kwargs.get('demo_delivery_email') == 'visitor@portfolio.com'

    @patch('routes.auth_apis.cache.set')
    @patch('routes.auth_apis.send_otp_email.delay')
    def test_auth_request_otp_real_user_ignores_demo_delivery(self, mock_delay, mock_cache, app_instance):
        """POST /api/auth/request-login-otp never routes to demo_delivery_email for real registered user."""
        client = app_instance.test_client()
        res = client.post('/api/auth/request-login-otp', json={
            'email': 'john@realuser.com',
            'demo_delivery_email': 'hacker@malicious.com'
        })
        assert res.status_code == 200
        mock_delay.assert_called_once()
        kwargs = mock_delay.call_args[1]
        assert kwargs.get('demo_delivery_email') is None
