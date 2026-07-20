from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker


DB_URL = "sqlite:///fastapi.db"
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    
Base.metadata.create_all(bind=engine)


print("Database and tables created!")