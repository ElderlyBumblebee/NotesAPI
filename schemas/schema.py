from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    name: str
    phone_number: str
    email: EmailStr

class UserCreate(UserSchema):
    password: str  # нужен для регистрации, но не для ответа

class UserUpdate(UserSchema):
    id: int
    class Config:
            from_attributes = True

class UserDelete(UserSchema):
    pass
class UserResponse(UserSchema):
    id: int
    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str