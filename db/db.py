from sqlalchemy import create_engine
from sqlmodel import Session

eng = 'database.db'

sqlite_url = 'postgresql://gems_user:trOhcs6W67OARwm1rgyHWzCO2dQvBY1Z@dpg-clu784a1hbls73eb0f00-a.oregon-postgres.render.com/gems'
engine = create_engine(sqlite_url, echo=True)
session = Session(bind=engine)