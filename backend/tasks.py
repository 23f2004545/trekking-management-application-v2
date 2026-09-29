import csv
import io
import os
import base64
import ssl
from datetime import datetime, timedelta
from celery import Celery
from celery.schedules import crontab
from controller.extensions import db
from controller.models import User, Booking, Trek
from routes.utils_apis import create_notification
from sqlalchemy import func, extract
from mail import send_html_email
from config import config
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

broker_url = config.CELERY_BROKER_URL
result_backend = config.CELERY_RESULT_BACKEND

celery_app = Celery('tasks', broker=broker_url, backend=result_backend)

celery_config = {
    'timezone': 'Asia/Kolkata',  # Standard tzdata name for IST
    'enable_utc': False,
    'task_always_eager': config.CELERY_TASK_ALWAYS_EAGER,
    'beat_schedule': {
        'daily-trek-reminder-8am': {
            'task': 'tasks.daily_trek_reminder',
            'schedule': crontab(hour=8, minute=0), # Fires exactly at 8:00 AM IST
        },
        'monthly-admin-report-1st': {
            'task': 'tasks.monthly_admin_report',
            'schedule': crontab(day_of_month='1', hour=9, minute=0), # 1st of month at 9:00 AM
        }
    }
}

if broker_url and broker_url.startswith('rediss://'):
    celery_config['broker_use_ssl'] = {'ssl_cert_reqs': ssl.CERT_NONE}
    celery_config['redis_backend_use_ssl'] = {'ssl_cert_reqs': ssl.CERT_NONE}

celery_app.conf.update(celery_config)

FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://trekking-management-application-v2-snowy.vercel.app").rstrip("/")


def send_brevo_email(target_email, target_name, subject, html_body, filename=None, file_string_data=None):
    """
    Unified HTTP Email Delivery Engine using Brevo SDK.
    Bypasses SMTP port blocks automatically.
    """
    api_key = config.BREVO_API_KEY or os.environ.get("BREVO_API_KEY")
    if not api_key:
        print(f"⚠️ [BREVO UNCONFIGURED] BREVO_API_KEY is not set. Falling back to SMTP/Console logger.")
        return send_html_email(target_email, subject, html_body, filename, file_string_data.encode('utf-8') if isinstance(file_string_data, str) else file_string_data)

    # 1. Configure the API client
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    # 2. Build Sender and Recipient envelopes
    # Cloud providers like Brevo require the sender email to match a verified sender address
    sender_email = config.BREVO_SENDER_EMAIL or config.SMTP_SENDER_EMAIL or config.SMTP_USER or "nohara1887@gmail.com"
    sender_name = config.BREVO_SENDER_NAME or config.SMTP_SENDER_NAME or "Apex Expeditions"
    sender_details = {"name": sender_name, "email": sender_email}
    recipient_details = [{"email": target_email, "name": target_name or target_email}]
    
    # 3. Handle File Attachment if present
    attachments = []
    if filename and file_string_data:
        file_bytes = file_string_data.encode('utf-8') if isinstance(file_string_data, str) else file_string_data
        b64_content = base64.b64encode(file_bytes).decode('utf-8')
        attachments.append({
            "name": filename,
            "content": b64_content
        })
        
    # 4. Compile the transaction payload
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=recipient_details,
        sender=sender_details,
        subject=subject,
        html_content=html_body,
        attachment=attachments if attachments else None
    )
    
    # 5. Dispatch over safe HTTPS (Port 443)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"[BREVO SUCCESS] Transmission acknowledged! MessageID: {api_response.message_id} -> {target_email} from {sender_email}")
        return True
    except ApiException as e:
        print(f"[BREVO FAILURE] Failed to push payload through API gateway: {e}")
        # Global fallback print so logs don't completely swallow data during testing
        print(f"⚠️ [SMTP FALLBACK] To: {target_email} | Subject: {subject}")
        return False
    except Exception as e:
        print(f"[BREVO UNEXPECTED ERROR] {e}")
        return False



# ==========================================================
# 1. ASYNC: CSV HISTORY EXPORT (In-Memory)
# ==========================================================
@celery_app.task(name='tasks.export_history_csv')
def export_history_csv(user_id, user_email, user_name, demo_delivery_email=None):
    from app import create_app
    app = create_app()
    with app.app_context():
        bookings = Booking.query.filter_by(user_id=user_id).all()
        
        # Build CSV strictly in RAM
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(['Booking ID', 'Trek Name', 'Date Secured', 'Payment Status', 'Lifecycle Status', 'Total Paid (INR)'])
        
        for b in bookings:
            writer.writerow([
                f"#APX-B{b.booking_id}", b.trek.trek_name if b.trek else "N/A", 
                b.booking_date.strftime("%Y-%m-%d"), b.payment_status, b.status, b.total_amount
            ])
            
        csv_string_data = csv_buffer.getvalue()
        csv_buffer.close() # Free memory
        
        demo_banner = ""
        if demo_delivery_email:
            demo_banner = f"""
            <div style="background-color: #1e3a2b; border: 1px dashed #10b981; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; color: #a7f3d0;">
                [DEMO PREVIEW] Dispatched for portfolio demonstration to <code>{demo_delivery_email}</code>. Your email address was not saved in our database.
            </div>
            """

        # Curated HTML Template
        html_body = f"""
        <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #0b1f15; color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #198754;">
            <div style="background-color: #198754; padding: 20px; text-align: center;">
                <h2 style="margin: 0; color: #ffffff; letter-spacing: 1px;">Apex Expeditions Data Core</h2>
            </div>
            <div style="padding: 30px;">
                {demo_banner}
                <h3 style="margin-top: 0;">Hello {user_name},</h3>
                <p style="color: #a0aec0; line-height: 1.6;">Your requested expedition history matrix has been successfully compiled from our secure database servers.</p>
                <p style="color: #a0aec0; line-height: 1.6;">Attached to this transmission is the CSV telemetry file containing your complete route logs, financial transactions, and basecamp authorizations.</p>
                <br>
                <p style="color: #a0aec0; font-size: 12px; border-top: 1px solid #2d3748; padding-top: 15px;">Securely generated by the Apex Automated Worker Matrix.</p>
            </div>
        </div>
        """
        
        filename = f"Apex_History_Log_{datetime.now().strftime('%Y%m%d')}.csv"
        target_email = demo_delivery_email or user_email
        send_brevo_email(target_email, user_name, "Your Expedition History CSV is Ready", html_body, filename, csv_string_data)


# ==========================================================
# 2. SCHEDULED BEAT: DAILY REMINDER WITH CTA
# ==========================================================
@celery_app.task(name='tasks.daily_trek_reminder')
def daily_trek_reminder():
    from app import create_app
    app = create_app()
    with app.app_context():
        
        tomorrow = datetime.now().date() + timedelta(days=1)
        upcoming_treks = Trek.query.filter(db.func.date(Trek.start_date) == tomorrow).all()
        # upcoming_treks = Trek.query.filter(Trek.status == 'Completed').all()
        
        
        for trek in upcoming_treks:
            # Safely resolve Staff Guide name
            guide_name = "Assigned at Basecamp"
            if trek.assigned_staff_id:
                guide_user = User.query.get(trek.assigned_staff_id)
                if guide_user: guide_name = guide_user.name

            bookings = Booking.query.filter_by(trek_id=trek.trek_id, status='Booked').all()
            for b in bookings:
                html_body = f"""
                <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; background-color: #0f172a; color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #1e293b;">
                    <div style="background-color: #198754; padding: 25px; text-align: center;">
                        <h2 style="margin: 0; color: #ffffff; letter-spacing: 1px;">Final Departure Briefing </h2>
                        <p style="margin: 5px 0 0 0; color: #e2e8f0; font-size: 14px;">Your expedition begins tomorrow.</p>
                    </div>
                    
                    <div style="padding: 30px;">
                        <h3 style="margin-top: 0; color: #f8f9fa;">Greetings {b.user.name},</h3>
                        <p style="color: #cbd5e1; line-height: 1.6;">We are exactly 24 hours out from our departure. This automated message serves as your final verification checkpoint before we break ground. Please review your tactical trail manifest below and ensure you arrive at the designated basecamp by 6:00 AM sharp.</p>
                        
                        <div style="background-color: #1e293b; border-radius: 8px; padding: 20px; margin: 25px 0; border-left: 4px solid #10b981;">
                            <h4 style="margin: 0 0 15px 0; color: #7bf1a8; border-bottom: 1px solid #334155; padding-bottom: 10px;">Expedition Manifest</h4>
                            
                            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                                <tr>
                                    <td style="padding: 8px 0; color: #94a3b8;">Route Name</td>
                                    <td style="padding: 8px 0; color: #ffffff; text-align: right; font-weight: bold;">{trek.trek_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #94a3b8;">Location Grid</td>
                                    <td style="padding: 8px 0; color: #ffffff; text-align: right;">{trek.location}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #94a3b8;">Duration</td>
                                    <td style="padding: 8px 0; color: #ffffff; text-align: right;">{trek.duration_days} Days</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #94a3b8;">Party Headcount</td>
                                    <td style="padding: 8px 0; color: #ffffff; text-align: right;">{b.number_of_persons} Explorers</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; color: #94a3b8;">Assigned Guide</td>
                                    <td style="padding: 8px 0; color: #7bf1a8; text-align: right;">{guide_name}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="text-align: center; margin-top: 35px;">
                            <a href="{FRONTEND_URL}/portal/trekker/bookings" style="background-color: #10b981; color: #022c22; padding: 12px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 14px; display: inline-block;">View Reservation Details</a>
                        </div>
                    </div>
                </div>
                """
                send_brevo_email(b.user.email, b.user.name, f"Apex Departure: {trek.trek_name} Starts Tomorrow", html_body)

# ==========================================================
# 3. SCHEDULED BEAT: MONTHLY ADMIN REPORT
# ==========================================================
@celery_app.task(name='tasks.monthly_admin_report')
def monthly_admin_report():
    from app import create_app
    app = create_app()
    with app.app_context():
        now = datetime.now() 
        month_name = now.strftime('%B %Y')
        
        # 1. FETCH MONTHLY KPI (Key Performance Indicators)
        # Revenue this month
        monthly_revenue = db.session.query(func.sum(Booking.total_amount)).filter(
            extract('month', Booking.created_at) == now.month,
            extract('year', Booking.created_at) == now.year,
            Booking.payment_status == 'Paid'
        ).scalar() or 0

        # New Routes registered this month
        new_routes_count = Trek.query.filter(
            extract('month', Trek.created_at) == now.month,
            extract('year', Trek.created_at) == now.year
        ).count()
    
        # Participants accommodated this month (sum of number_of_persons in Bookings)
        participants_accommodated_count = db.session.query(func.sum(Booking.number_of_persons)).filter(
            extract('month', Booking.created_at) == now.month,
            extract('year', Booking.created_at) == now.year,
            Booking.payment_status == 'Paid'  # Or Booking.status == 'Booked', depending on your models
        ).scalar() or 0

        # New Trekkers registered this month
        new_users_count = User.query.filter(
            User.role.has(name='trekker'),
            extract('month', User.created_at) == now.month,
            extract('year', User.created_at) == now.year
        ).count()

        # 2. POPULAR TREK OF THE MONTH
        popular_trek_query = db.session.query(
            Trek.trek_name, func.count(Booking.booking_id).label('b_count')
        ).join(Booking).filter(
            extract('month', Booking.created_at) == now.month
        ).group_by(Trek.trek_id).order_by(db.desc('b_count')).first()

        popular_trek_name = popular_trek_query[0] if popular_trek_query else "N/A"

        # 3. RECENT LOGS GLIMPSE (Latest 5 bookings)
        recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
        logs_html = ""
        for b in recent_bookings:
            logs_html += f"""
            <tr style="border-bottom: 1px solid #2d3748;">
                <td style="padding: 10px; color: #a0aec0; font-size: 13px;">#APX-{b.booking_id}</td>
                <td style="padding: 10px; color: #ffffff; font-size: 13px;">{b.trek.trek_name}</td>
                <td style="padding: 10px; color: #7bf1a8; font-size: 13px; text-align: right;">₹{b.total_amount}</td>
            </tr>"""

        # 4. CURATED HTML TEMPLATE
        html_body = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 650px; margin: 0 auto; background-color: #0f172a; color: #ffffff; border-radius: 16px; overflow: hidden; border: 1px solid #1e293b;">
            <div style="background: linear-gradient(90deg, #198754, #10b981); padding: 30px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px; letter-spacing: 1px;">Admin Executive Summary</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">Platform Performance for {month_name}</p>
            </div>

            <div style="padding: 30px;">
                <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
                    <h4 style="margin: 0 0 10px 0; color: #7bf1a8;">🌙 Monthly Perspective</h4>

                    <p style="margin: 0 0 15px 0;">We have continued to operate effectively and expand our map this cycle. Here are your operational highlights:</p>
    
                    <ul style="margin: 0; padding-left: 20px; list-style-type: circle;">
                        <li style="margin-bottom: 10px;">
                            <span style="color: #cbd5e1;">Trail Expansion:</span> 
                            <strong style="color: #ffffff;">{new_routes_count}</strong> new routes.
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="color: #cbd5e1;">Field Operations:</span> 
                            <strong style="color: #ffffff;">{participants_accommodated_count}</strong> participants.
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="color: #cbd5e1;">Community Growth:</span> 
                            <strong style="color: #ffffff;">{new_users_count}</strong> new explorers.
                        </li>
                        <li style="margin-bottom: 0;">
                            <span style="color: #cbd5e1;">Top Destination:</span> 
                            The <strong style="color: #ffffff;">{popular_trek_name}</strong> trail .
                        </li>
                    </ul>
                </div>

                <table style="width: 100%; margin-bottom: 30px;">
                    <tr>
                        <td style="width: 50%; padding-right: 10px;">
                            <div style="border: 1px solid #334155; padding: 15px; border-radius: 10px; text-align: center;">
                                <span style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">Monthly Revenue</span>
                                <div style="font-size: 20px; font-weight: bold; color: #7bf1a8; margin-top: 5px;">₹{monthly_revenue:,.0f}</div>
                            </div>
                        </td>
                        <td style="width: 50%; padding-left: 10px;">
                            <div style="border: 1px solid #334155; padding: 15px; border-radius: 10px; text-align: center;">
                                <span style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">Routes Deployed</span>
                                <div style="font-size: 20px; font-weight: bold; color: #ffffff; margin-top: 5px;">{new_routes_count}</div>
                            </div>
                        </td>
                    </tr>
                </table>

                <h4 style="margin: 0 0 15px 0; border-bottom: 1px solid #334155; padding-bottom: 10px;">📋 Recent Activity Logs</h4>
                <table style="width: 100%; border-collapse: collapse;">
                    {logs_html}
                </table>

                <div style="text-align: center; margin-top: 40px;">
                    <a href="{FRONTEND_URL}/portal/admin/dashboard" 
                       style="background-color: #10b981; color: #022c22; padding: 14px 35px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 14px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                       Access Command Center Analytics
                    </a>
                </div>
            </div>
            
            <div style="background-color: #1e293b; padding: 15px; text-align: center; font-size: 11px; color: #64748b;">
                System generated report. Confidential administrative data.
            </div>
        </div>
        """
        
        admin = User.query.filter(User.role.has(name='admin')).first()
        create_notification(admin.id, "Monthly executive report generated and emailed.", "info")
        send_brevo_email(admin.email, admin.name, f"Platform Audit Report: {month_name}", html_body)
        
        

# ==========================================================
# 4. ASYNC: OTP EMAIL FOR PASSWORD RESET
# ==========================================================
@celery_app.task(name='tasks.send_otp_email')
def send_otp_email(user_email, user_name, otp_code, demo_delivery_email=None):
    demo_banner = ""
    if demo_delivery_email:
        demo_banner = f"""
        <div style="background-color: #e6f4ea; border: 1px dashed #198754; padding: 10px; border-radius: 6px; margin-bottom: 15px; font-size: 12px; color: #0f5132;">
            [DEMO PREVIEW] Dispatched for portfolio demonstration to {demo_delivery_email}. Your email address was not saved in our database.
        </div>
        """
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; border: 1px solid #e2e8f0; padding: 30px; text-align: center; border-radius: 8px;">
        {demo_banner}
        <h2 style="color: #1a202c; margin-top: 0;">Security Verification</h2>
        <p style="color: #4a5568;">Hello {user_name},</p>
        <p style="color: #4a5568;">A request was made to reset your Apex Expeditions security key. Your one-time authorization code is:</p>
        <div style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #198754; background-color: #f0fdf4; padding: 15px; margin: 20px 0; border-radius: 8px;">
            {otp_code}
        </div>
        <p style="color: #a0aec0; font-size: 13px;">This code will self-destruct in exactly 5 minutes. If you did not request this, please ignore this transmission.</p>
    </div>
    """
    target_email = demo_delivery_email or user_email
    send_brevo_email(target_email, user_name, "Apex Security: Your Password Reset Code", html_body)

     
# ==========================================================
# 5. ASYNC: SEND CREDENTIALS TO CANDIDATE
# ==========================================================    
@celery_app.task(name='tasks.send_staff_credentials_email')
def send_staff_credentials_email(personal_email, staff_email, staff_password, demo_delivery_email=None):
    from app import create_app
    app = create_app()
    with app.app_context():
        demo_banner = ""
        if demo_delivery_email:
            demo_banner = f"""
            <div style="background-color: #1e3a2b; border: 1px dashed #10b981; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; color: #a7f3d0;">
                [DEMO PREVIEW] Dispatched for portfolio demonstration to <code>{demo_delivery_email}</code>. Your email address was not saved in our database.
            </div>
            """
        html_body = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; background-color: #0f172a; color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #1e293b;">
            <div style="background-color: #198754; padding: 25px; text-align: center;">
                <h2 style="margin: 0; color: #ffffff; letter-spacing: 1px;">Apex Basecamp Authorization</h2>
                <p style="margin: 5px 0 0 0; color: #e2e8f0; font-size: 14px;">Your tactical guide account has been deployed.</p>
            </div>
            
            <div style="padding: 30px;">
                {demo_banner}
                <h3 style="margin-top: 0; color: #f8f9fa;">Welcome Commander,</h3>
                <p style="color: #cbd5e1; line-height: 1.6;">Administration has provisioned your secure portal access. You are now authorized to manage expedition manifests, update live trail parameters, and clear explorer medical passports.</p>
                
                <div style="background-color: #1e293b; border-radius: 8px; padding: 20px; margin: 25px 0; border-left: 4px solid #10b981;">
                    <h4 style="margin: 0 0 15px 0; color: #7bf1a8; border-bottom: 1px solid #334155; padding-bottom: 10px;">Initial Access Credentials</h4>
                    <p style="margin: 0 0 8px 0; color: #94a3b8; font-size: 14px;"><strong>Portal Node:</strong> <a href="{FRONTEND_URL}/login" style="color: #7bf1a8; text-decoration: underline;">{FRONTEND_URL}/login</a></p>
                    <p style="margin: 0 0 8px 0; color: #94a3b8; font-size: 14px;"><strong>Assigned Email:</strong> <span style="color: #fff;">{staff_email}</span></p>
                    <p style="margin: 0; color: #94a3b8; font-size: 14px;"><strong>Temporary Key:</strong> <span style="color: #ffda6a; font-family: monospace; font-size: 16px;">{staff_password}</span></p>
                </div>

                <p style="color: #ff8787; font-size: 12px; margin-top: 20px;">[Notice] Mandatory Compliance: You are required to mutate your security key immediately upon your first terminal login.</p>
            </div>
        </div>
        """
        target_email = demo_delivery_email or personal_email
        send_brevo_email(target_email, "Field Staff Candidate", "Apex Expeditions: Guide Account Credentials", html_body)
        

# ==========================================================
# 6. ASYNC : RAISED TICKET RESOLVED EMAIL TO USER
# ==========================================================  
@celery_app.task(name='tasks.dispatch_ticket_resolution')
def dispatch_ticket_resolution(user_email, user_name, user_role, subject, original_message, admin_response, demo_delivery_email=None):
    from datetime import datetime
    
    # Adjust tone slightly based on role
    salutation = "Field Commander" if user_role == 'trek_staff' else "Explorer"
    role_color = "#ffda6a" if user_role == 'trek_staff' else "#7bf1a8"

    demo_banner = ""
    if demo_delivery_email:
        demo_banner = f"""
        <div style="background-color: #1e3a2b; border: 1px dashed #10b981; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; color: #a7f3d0;">
            [DEMO PREVIEW] Dispatched for portfolio demonstration to <code>{demo_delivery_email}</code>. Your email address was not saved in our database.
        </div>
        """

    html_body = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #050a08; color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #198754;">
        <div style="background-color: #198754; padding: 25px; text-align: center; border-bottom: 3px solid {role_color};">
            <h2 style="margin: 0; color: #ffffff; letter-spacing: 2px; font-size: 18px; text-transform: uppercase;">Central Command Resolution</h2>
            <p style="margin: 5px 0 0 0; color: #e2e8f0; font-size: 13px;">Official Dispatch Response</p>
        </div>
        
        <div style="padding: 30px;">
            {demo_banner}
            <p style="color: #cbd5e1; font-size: 15px;">Greetings {salutation} {user_name},</p>
            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">Your recent operational query has been reviewed and resolved by Apex Administration. Please review the official directive below.</p>
            
            <div style="background-color: rgba(255,255,255,0.03); padding: 20px; border-radius: 8px; margin: 25px 0; border: 1px solid rgba(255,255,255,0.1);">
                <span style="color: #64748b; font-size: 10px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">Original Subject Vector</span>
                <h4 style="margin: 5px 0 15px 0; color: #ffffff;">{subject}</h4>
                
                <span style="color: #64748b; font-size: 10px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">Your Transmission</span>
                <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 13px; font-style: italic; border-left: 2px solid #334155; padding-left: 10px;">"{original_message}"</p>
            </div>
            
            <div style="background-color: rgba(25,135,84,0.1); padding: 20px; border-radius: 8px; border-left: 4px solid #198754; margin: 25px 0;">
                <span style="color: #7bf1a8; font-size: 11px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">Command Directive</span>
                <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 15px; line-height: 1.6;">{admin_response}</p>
            </div>
            
            <p style="color: #64748b; font-size: 13px; text-align: center; margin-top: 35px; border-top: 1px solid #1e293b; padding-top: 20px;">
                Resolution Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}<br>
                For further assistance, initiate a new dispatch via your secure terminal.
            </p>
        </div>
    </div>
    """
    target_email = demo_delivery_email or user_email
    send_brevo_email(target_email, user_name, f"Resolved: {subject}", html_body)


# ==========================================================
# 7. ASYNC : EXPORT TREK SPECIFIC INSIGHTS AFTER COMPLETION
# ==========================================================  
@celery_app.task(name='tasks.export_history_telemetry')
def export_history_telemetry(admin_email, admin_name, payload, demo_delivery_email=None):
    trek_meta = payload.get('trek_info') or payload.get('trek') or {}
    analytics = payload.get('analytics', {})
    staff = payload.get('staff_info') or payload.get('staff') or {}
    trek_name = trek_meta.get('name') or trek_meta.get('trek_name') or 'Expedition'
    
    demo_banner = ""
    if demo_delivery_email:
        demo_banner = f"""
        <div style="background-color: #1e3a2b; border: 1px dashed #10b981; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; color: #a7f3d0;">
            [DEMO PREVIEW] Dispatched for portfolio demonstration to <code>{demo_delivery_email}</code>. Your email address was not saved in our database.
        </div>
        """

    html_body = f"""
    <div style="font-family: 'Consolas', 'Courier New', monospace; max-width: 650px; margin: 0 auto; background-color: #050a08; color: #cbd5e1; border-radius: 8px; border: 1px solid #198754; overflow: hidden;">
        
        <div style="background-color: #0b1f15; padding: 20px; border-bottom: 2px solid #7bf1a8; text-align: left;">
            <h2 style="margin: 0; color: #ffffff; letter-spacing: 2px; text-transform: uppercase;">APEX OPERATIONS</h2>
            <p style="margin: 5px 0 0 0; color: #7bf1a8; font-size: 12px;">Archived Telemetry Export // CONFIDENTIAL</p>
        </div>
        
        <div style="padding: 30px;">
            {demo_banner}
            <p style="color: #ffffff;">Authorized Requestor: <strong>{admin_name}</strong></p>
            <p style="font-size: 13px; color: #94a3b8; border-bottom: 1px solid #1e293b; padding-bottom: 15px;">The following data packet contains the operational yield and manifest overview for the requested historical deployment.</p>
            
            <h3 style="color: #ffffff; margin-top: 25px; border-left: 3px solid #7bf1a8; padding-left: 10px;">SECTOR: {trek_name}</h3>
            <table style="width: 100%; font-size: 13px; margin-bottom: 20px; background: rgba(255,255,255,0.02); padding: 10px;">
                <tr>
                    <td style="padding: 5px 0; color: #64748b;">DURATION:</td><td style="color: #ffffff; text-align: right;">{trek_meta.get('duration', 'N/A')} Days</td>
                </tr>
                <tr>
                    <td style="padding: 5px 0; color: #64748b;">ALTITUDE:</td><td style="color: #ffffff; text-align: right;">{trek_meta.get('altitude', 'N/A')}m</td>
                </tr>
                <tr>
                    <td style="padding: 5px 0; color: #64748b;">TIMELINE:</td><td style="color: #ffffff; text-align: right;">{trek_meta.get('start_date', 'N/A')} to {trek_meta.get('end_date', 'N/A')}</td>
                </tr>
            </table>

            <h3 style="color: #ffffff; margin-top: 25px; border-left: 3px solid #198754; padding-left: 10px;">ASSIGNED COMMANDER</h3>
            <p style="margin: 5px 0; font-size: 14px; color: #7bf1a8;">{staff.get('name', 'Unassigned')}</p>
            <p style="margin: 0; font-size: 12px; color: #94a3b8;">ID: {staff.get('email', 'N/A')} | Clearance: {staff.get('certification', 'Standard')}</p>

            <h3 style="color: #ffffff; margin-top: 35px; border-bottom: 1px solid #1e293b; padding-bottom: 5px;">OPERATIONAL YIELD</h3>
            
            <table style="width: 100%; border-collapse: separate; border-spacing: 10px 0; margin-top: 15px;">
                <tr>
                    <td style="width: 50%; background: #0b1f15; padding: 15px; border: 1px solid #198754; border-radius: 6px; text-align: center;">
                        <span style="display: block; font-size: 10px; color: #7bf1a8; letter-spacing: 1px;">GROSS REVENUE</span>
                        <strong style="font-size: 18px; color: #ffffff;">INR {analytics.get('total_revenue', 0)}</strong>
                    </td>
                    <td style="width: 50%; background: #1e1b15; padding: 15px; border: 1px solid #9a3412; border-radius: 6px; text-align: center;">
                        <span style="display: block; font-size: 10px; color: #fdba74; letter-spacing: 1px;">DROPS / CANCELLATIONS</span>
                        <strong style="font-size: 18px; color: #ffffff;">{analytics.get('cancelled_participants', 0)} Pax</strong>
                    </td>
                </tr>
            </table>
            
            <table style="width: 100%; font-size: 13px; margin-top: 20px;">
                <tr>
                    <td style="padding: 8px 0; border-bottom: 1px dotted #334155;">Explorers Cleared:</td>
                    <td style="text-align: right; border-bottom: 1px dotted #334155; color: #ffffff;">{analytics.get('completed_participants', 0)}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; border-bottom: 1px dotted #334155;">Distinct Passports:</td>
                    <td style="text-align: right; border-bottom: 1px dotted #334155; color: #ffffff;">{analytics.get('accounts_booked', 0)}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; border-bottom: 1px dotted #334155;">Completion Rate:</td>
                    <td style="text-align: right; border-bottom: 1px dotted #334155; color: #7bf1a8;">{analytics.get('completion_rate', 100)}%</td>
                </tr>
            </table>

            <p style="font-size: 11px; color: #475569; text-align: center; margin-top: 40px;">End of Transmission.<br>Generated automatically by Apex System Architecture.</p>
        </div>
    </div>
    """
    target_email = demo_delivery_email or admin_email
    send_brevo_email(target_email, admin_name, f"Archived Telemetry: {trek_name}", html_body)


# ==========================================================
# 8. ASYNC : TREK COMPLETION/CANCELLATION MAIL
# ==========================================================  
@celery_app.task(name='tasks.dispatch_cancellation_email')
def dispatch_cancellation_email(user_email, user_name, trek_name, duration, reason, cancelled_by="Administration", demo_delivery_email=None):
    demo_banner = ""
    if demo_delivery_email:
        demo_banner = f"""
        <div style="background-color: #2b1e1e; border: 1px dashed #ef4444; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; color: #fca5a5;">
            [DEMO PREVIEW] Dispatched for portfolio demonstration to <code>{demo_delivery_email}</code>. Your email address was not saved in our database.
        </div>
        """

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #0a0a0a; color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #7f1d1d;">
        <div style="background-color: #7f1d1d; padding: 25px; text-align: center; border-bottom: 3px solid #ef4444;">
            <h2 style="margin: 0; color: #ffffff; letter-spacing: 2px; font-size: 18px; text-transform: uppercase;">Expedition Aborted</h2>
            <p style="margin: 5px 0 0 0; color: #fca5a5; font-size: 13px;">Official Cancellation Notice</p>
        </div>
        <div style="padding: 30px;">
            {demo_banner}
            <p style="color: #cbd5e1; font-size: 15px;">Explorer {user_name},</p>
            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">We deeply regret to inform you that your upcoming <strong>{duration}-Day</strong> expedition to <strong>{trek_name}</strong> has been officially halted by {cancelled_by}.</p>
            
            <div style="background-color: rgba(239, 68, 68, 0.1); padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444; margin: 25px 0;">
                <span style="color: #fca5a5; font-size: 11px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">Declaration of Cancellation</span>
                <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 14px; line-height: 1.6;">"{reason}"</p>
            </div>
            
            <p style="color: #94a3b8; font-size: 13px;">Your payment status has been shifted to the refund pipeline. We apologize for the operational disruption. True alpine environments require absolute safety compliance.</p>
            
            <div style="text-align: center; margin-top: 35px;">
                <a href="{FRONTEND_URL}/" style="background-color: #ffffff; color: #000000; padding: 12px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 13px; display: inline-block;">Explore Alternate Routes</a>
            </div>
        </div>
    </div>
    """
    target_email = demo_delivery_email or user_email
    send_brevo_email(target_email, user_name, f"CRITICAL: {trek_name} Cancelled", html_body)

@celery_app.task(name='tasks.dispatch_completion_email')
def dispatch_completion_email(user_email, user_name, trek_name, duration, altitude, demo_delivery_email=None):
    demo_banner = ""
    if demo_delivery_email:
        demo_banner = f"""
        <div style="background-color: #1e3a2b; border: 1px dashed #10b981; padding: 10px 15px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; color: #a7f3d0;">
            [DEMO PREVIEW] Dispatched for portfolio demonstration to <code>{demo_delivery_email}</code>. Your email address was not saved in our database.
        </div>
        """

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #050a08; color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #198754;">
        <div style="background-color: #198754; padding: 25px; text-align: center; border-bottom: 3px solid #7bf1a8;">
            <h2 style="margin: 0; color: #ffffff; letter-spacing: 2px; font-size: 18px; text-transform: uppercase;">Expedition Concluded</h2>
            <p style="margin: 5px 0 0 0; color: #e2e8f0; font-size: 13px;">Welcome back to Basecamp.</p>
        </div>
        <div style="padding: 30px;">
            {demo_banner}
            <p style="color: #cbd5e1; font-size: 15px;">Congratulations {user_name},</p>
            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">Your <strong>{duration}-Day</strong> deployment to <strong>{trek_name}</strong> has been officially marked as completed by your Field Commander.</p>
            
            <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="margin: 25px 0; border-collapse: separate; border-spacing: 10px 0;">
                <tr>
                    <td width="50%" style="background: rgba(255,255,255,0.03); padding: 15px; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; text-align: center;">
                        <span style="display: block; font-size: 10px; color: #7bf1a8; letter-spacing: 1px; text-transform: uppercase; font-weight: bold;">Peak Altitude</span>
                        <strong style="font-size: 20px; color: #ffffff;">{altitude}m</strong>
                    </td>
                    <td width="50%" style="background: rgba(255,255,255,0.03); padding: 15px; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; text-align: center;">
                        <span style="display: block; font-size: 10px; color: #7bf1a8; letter-spacing: 1px; text-transform: uppercase; font-weight: bold;">Status</span>
                        <strong style="font-size: 20px; color: #ffffff;">CLEARED</strong>
                    </td>
                </tr>
            </table>
            
            <p style="color: #94a3b8; font-size: 13px; text-align: center;">Your telemetry data assists future explorers. We request you log an official terrain and commander evaluation.</p>
            
            <div style="text-align: center; margin-top: 25px;">
                <a href="{FRONTEND_URL}/portal/trekker/history" style="background-color: #7bf1a8; color: #0b1f15; padding: 12px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 13px; display: inline-block;">Log Official Review</a>
            </div>
        </div>
    </div>
    """
    target_email = demo_delivery_email or user_email
    send_brevo_email(target_email, user_name, f"Expedition Cleared: {trek_name}", html_body)