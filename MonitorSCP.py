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

def send_email_notification():
    msg = MIMEText("Failed to associate with Echo SCP!")
    msg["Subject"] = "DICOM Association Notification"
    msg["From"] = email_sender
    msg["To"] = email_reciver

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, password)
        server.send_message(msg)
        print("Email enviado correctamente")

def check_dicom_association():
    ae = AE()  # creates a new AE instance
    ae.add_requested_context("1.2.840.10008.1.1")

    assoc = ae.associate("127.0.0.1", 11112)

    if assoc.is_established:
        print("Association established with Echo SCP!")
        assoc.release()
    else:
        print("Failed to associate")
        send_email_notification()

# Schedule the function to run every 5 minutes
schedule.every(1).minutes.do(check_dicom_association)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
