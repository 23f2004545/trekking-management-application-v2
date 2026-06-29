import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Mailpit Default Configuration
SMTP_HOST = '127.0.0.1'
SMTP_PORT = 1025
SENDER_EMAIL = 'operations@apex-expeditions.com'
SENDER_NAME = 'Apex Expeditions'

def send_html_email(to_email, subject, html_content, attachment_name=None, attachment_data=None):
    
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg['To'] = to_email

    # Attach the HTML Body
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    # Attach the In-Memory CSV if provided
    if attachment_name and attachment_data:
        # Convert string data to bytes for the attachment payload
        part = MIMEApplication(attachment_data.encode('utf-8'))
        part.add_header('Content-Disposition', 'attachment', filename=attachment_name)
        msg.attach(part)

    # Execute SMTP Handshake
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            # No TLS or Login required for local Mailpit testing
            server.send_message(msg)
            print(f"📧 [SMTP SUCCESS] Delivered '{subject}' to {to_email}")
            return True
    except Exception as e:
        print(f"❌ [SMTP FAILURE] Drop detected: {str(e)}")
        return False