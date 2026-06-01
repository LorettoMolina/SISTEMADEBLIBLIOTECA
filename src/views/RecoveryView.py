import random
import smtplib
import os

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

codigo_recuperacion = ""

def enviar_codigo(correo_destino):

    global codigo_recuperacion

    codigo_recuperacion = str(
        random.randint(100000,999999)
    )

    mensaje = MIMEText(
        f"Tu código es: {codigo_recuperacion}"
    )

    mensaje["Subject"] = "Recuperación"
    mensaje["From"] = MAIL_USER
    mensaje["To"] = correo_destino

    servidor = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    servidor.starttls()

    servidor.login(
        MAIL_USER,
        MAIL_PASSWORD
    )

    servidor.send_message(
        mensaje
    )

    servidor.quit()

    return codigo_recuperacion