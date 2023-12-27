from sqlalchemy import create_engine
from sqlmodel import Session
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

postgres_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(postgres_url, echo=True)
session = Session(bind=engine)