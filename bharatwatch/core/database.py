from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bharatwatch.core.models import Base
from bharatwatch.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
