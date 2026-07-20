from fastapi import FastAPI, Depends, HTTPException

from models.model import engine, SessionLocal, User

from schemas.schema import UserSchema, UserResponse, UserCreate

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=list[UserResponse])
def get_users(db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    return users;

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_in: UserCreate, db: SessionLocal= Depends(get_db)):
    new_user = User(**user_in.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
