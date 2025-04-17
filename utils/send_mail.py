from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from dotenv import load_dotenv
from mail_templates.verifyEmailonregister import verificationLink_onRegister
load_dotenv()
import os
from mail_templates.loginalertonLogIn import login_alert_html
#from pathlib import Path
#logo_path = Path(__file__).parent / "logo.png" 




conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="vikash", #your name
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_verification_email_atREgistration_time(email:EmailStr, token:str):
    message = MessageSchema(
        subject="Verify our Email",
        recipients=[email],
        body=verificationLink_onRegister(email,token),
        subtype="html"  
    )
    print(os.getenv("MAIL_USERNAME"))
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_login_alert(name,email,location,time):
    message = MessageSchema(
        subject="New logIN",
        recipients=[email],
        body=login_alert_html(name,location,time),
        subtype="html",
        
    )

    fm = FastMail(conf)  
    await fm.send_message(message)