from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()
engine = create_engine('sqlite:///FastAPIbase.db', echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50))
    patronomic = Column(String(50))
    phone_number = Column(String(20), unique=True, nullable=True)   
    email = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name} {self.surname}>"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)