from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase

DB_URL = "sqlite:///fastapi.db"
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

Base.metadata.create_all(bind=engine)