from app.models.seller_models import MailBody, Seller
from app.repos.config import HOST, USERNAME, PASSWORD, PORT
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP
from sqlmodel import Session
from app.db.db import engine
from app.models.gem_models import Gem


def send_mail(data: dict | None = None):
    msg = MailBody(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = USERNAME
    message["To"] = ",".join(msg.to)
    message["Subject"] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}
    
def seller_gem(data: Seller):
    with Session(engine) as session:
        gem_found = session.get(Gem, data.id)
        gem_found.quantity = gem_found.quantity - data.quantity

        if gem_found.quantity == 0:
            gem_found.available == False
        
        session.commit()
        session.refresh(gem_found)

        if gem_found.quantity == 0:
            gem_found.available == False

            session.commit()
            session.refresh(gem_found)
            
        if gem_found:
            return gem_found