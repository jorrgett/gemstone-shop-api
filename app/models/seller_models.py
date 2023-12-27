from typing import List
from fastapi import Body
from pydantic import BaseModel

class MailBody(BaseModel):
    subject: str = Body(...)
    emailAddress: str = Body(...)
    message: str = Body(...)