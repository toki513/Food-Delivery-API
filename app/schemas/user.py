from pydantic import BaseModel,EmailStr,Field,field_validator
import uuid
from app.models.user import UserRole


class UserCreate(BaseModel):
    email:EmailStr
    full_name:str
    password:str
    role:UserRole=UserRole.CUSTOMER
    phone:str|None
    
    @field_validator("password")
    @classmethod
    def password_strength(cls,v:str)->str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:uuid.UUID
    email:str
    full_name:str
    phone:str|None
    role:UserRole
    is_active:bool
    is_verified:bool
    profile_image:str|None
    
    model_config={"from_attributes":True}
    
class UserUpdate(BaseModel):
    full_name:str|None
    phone:str|None
    
    
class UserAdminUpdate(UserUpdate):
    role:UserRole|None=None
    is_active:bool|None=None