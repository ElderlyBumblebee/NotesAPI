from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import bcrypt
import uvicorn

from models.model import SessionLocal, User
from schemas.schema import (
    UserSchema, UserResponse, UserCreate, UserUpdate, UserDelete,
    UserLoginSchema, TokenResponse,
)

from authx import AuthX, AuthXConfig

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login", response_model=TokenResponse, tags=["Authentication"])
def login(creds: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.execute(
        select(User).where(User.email == creds.email)
    ).scalar_one_or_none()

    if user is None or not bcrypt.checkpw(creds.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect password or email")

    token = security.create_access_token(uid=str(user.id))
    return {"access_token": token}


@app.get("/protected", dependencies=[Depends(security.access_token_required)], tags=["Authentication"])
def protected():
    return {"message": "You authorized"}


@app.get("/users", response_model=list[UserResponse], tags=["UserEndpoints"])
def get_users(db: Session = Depends(get_db)):
    users = db.execute(select(User)).scalars().all()
    return users


@app.post("/users", response_model=UserResponse, status_code=201, tags=["UserEndpoints"])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user_in.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = User(
        name=user_in.name,
        phone_number=user_in.phone_number,
        email=user_in.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.put("/users/{user_id}", response_model=UserResponse, tags=["UserEndpoints"])
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.model_dump().items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}", tags=["UserEndpoints"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)