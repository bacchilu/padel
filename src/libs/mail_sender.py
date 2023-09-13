import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .utils import log_console


SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "bacchilu@gmail.com")
SENDER_PWD = os.environ.get("SENDER_PWD", "PWD")
SUBJECT = "Padel Notification System"


SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))


def send_mail(receiver_email: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    try:
        server.starttls()  # Start TLS encryption
        server.login(SENDER_EMAIL, SENDER_PWD)

        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, receiver_email, text)
    except Exception as e:
        log_console(f"Email could not be sent. Error: {str(e)}")
    finally:
        server.quit()
