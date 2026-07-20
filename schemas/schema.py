from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    name : str
    phone_number : str
    email : EmailStr
    
class UserCreate(UserSchema):
    pass

class UserResponse(UserSchema):
    id : int 
    
    class Config:
        from_attributes = True


