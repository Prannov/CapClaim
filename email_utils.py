import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_claim_email(to_email, name, claim_type):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")

    subject = "Claim Submission Confirmation"
    body = f"""
    Hi {name},

    Your {claim_type} insurance claim has been successfully submitted to CapClaim.

    We'll reach out if we need more information. Thanks for using CapClaim!

    Regards,
    CapClaim Team
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent to", to_email)
    except Exception as e:
        print("Failed to send email:", e)
