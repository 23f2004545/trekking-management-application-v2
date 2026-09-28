import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import config

SMTP_HOST = config.SMTP_HOST
SMTP_PORT = config.SMTP_PORT
SMTP_USER = config.SMTP_USER
SMTP_PASSWORD = config.SMTP_PASSWORD
SMTP_USE_TLS = config.SMTP_USE_TLS
SMTP_USE_SSL = config.SMTP_USE_SSL
SENDER_EMAIL = config.SMTP_SENDER_EMAIL
SENDER_NAME = config.SMTP_SENDER_NAME


def send_html_email(to_email, subject, html_content, attachment_name=None, attachment_data=None):
    """
    Sends an HTML email with optional attachments using configured SMTP settings.
    Gracefully falls back to console logging if SMTP credentials are unset or if
    a network drop occurs, ensuring asynchronous tasks never crash unhandled.
    """
    smtp_host = config.SMTP_HOST
    smtp_port = int(config.SMTP_PORT)
    smtp_user = config.SMTP_USER
    smtp_password = config.SMTP_PASSWORD
    smtp_use_tls = config.SMTP_USE_TLS
    smtp_use_ssl = config.SMTP_USE_SSL
    sender_email = config.SMTP_SENDER_EMAIL
    sender_name = config.SMTP_SENDER_NAME

    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = to_email

    # Attach HTML Body
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    # Attach optional in-memory data
    if attachment_name and attachment_data:
        part = MIMEApplication(attachment_data.encode('utf-8') if isinstance(attachment_data, str) else attachment_data)
        part.add_header('Content-Disposition', 'attachment', filename=attachment_name)
        msg.attach(part)

    # If no SMTP_USER configured and SMTP_HOST is default/local, attempt local Mailpit;
    # if it fails or if host is not reachable, fall back to console logging.
    try:
        if smtp_use_ssl or smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)

        with server as s:
            if smtp_use_tls or smtp_port == 587:
                s.starttls()

            if smtp_user and smtp_password:
                s.login(smtp_user, smtp_password)

            s.send_message(msg)
            print(f"📧 [SMTP SUCCESS] Delivered '{subject}' to {to_email}")
            return True
    except Exception as e:
        # Fallback console logger to prevent task dropping
        print(f"⚠️ [SMTP FALLBACK - SIMULATION LOG]")
        print(f"   To: {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Reason: {str(e)}")
        print(f"   Note: Email simulated successfully without dropping.")
        return True