import schedule
import time
from pynetdicom import AE, debug_logger
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl

load_dotenv()

email_sender = "ge.dardo@gmail.com"
password = os.getenv("PASSWORD")
email_reciver = "gcollado@impulso-mexicano.com"

previous_status = None

def send_email_notification(status):
    msg = MIMEText(f"Association status: {status}")
    msg["Subject"] = "DICOM Association Notification"
    msg["From"] = email_sender
    msg["To"] = email_reciver

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, password)
        server.send_message(msg)
        print("Email enviado correctamente")

def check_dicom_association():
    global previous_status
    ae = AE()  # creates a new AE instance
    ae.add_requested_context("1.2.840.10008.1.1")

    assoc = ae.associate("127.0.0.1", 11112)

    if assoc.is_established:
        current_status = "established"
        print("Association established with Echo SCP!")
        assoc.release()
    else:
        current_status = "failed"
        print("Failed to associate")

    if current_status != previous_status:
        send_email_notification(current_status)
        previous_status = current_status

# Schedule the function to run every 5 minutes
schedule.every(1).minutes.do(check_dicom_association)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
