import smtplib
from fastapi import APIRouter
from app.auth.auth import AuthHandler
from app.models.seller_models import MailBody
from email.message import EmailMessage

from app.repos.config import PASSWORD, USERNAME

seller_router = APIRouter()
auth_handler = AuthHandler()

@seller_router.post(
        path='/email',
        status_code=201,
        tags=['Seller'],
        summary='Send Email'
)
def send_email(data: MailBody):
 
    email_address = USERNAME
    email_password = PASSWORD
 
    msg = EmailMessage()
    msg['Subject'] = data.subject
    msg['From'] = email_address
    msg['To'] = data.emailAddress
    msg.set_content(
       f"""\
    {data.message}    
    """,
         
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
 
    return "email successfully sent"