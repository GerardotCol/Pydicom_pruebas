import os
from email.message import EmailMessage
import ssl
import smtplib



email_sender = "ge.dardo@gmail.com"
password =  "ktigzhaedxejfbrk"
emal_reciver = "gcollado@impulso-mexicano.com"

subject = "Suscribete a mi canal"
body = '''

Asi que nada chavales aqui no se que poner y poco mas...
'''

em = EmailMessage()
em["From"] = email_sender
em["To"] = emal_reciver
em["Subject"] = subject
em. set_content (body)
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_sender, password)
    server.send_message(em)
    print("Email enviado correctamente")