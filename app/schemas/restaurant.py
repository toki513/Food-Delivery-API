import uuid
from pydantic import BaseModel,Field


class RestaurantCreate(BaseModel):
    name:str
    description:str
    address:str
    phone:str
    cuisine_type:str|None
    delivery_fee:float
    minimum_order:float
    
class RestaurantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    address: str | None = Field(default=None, min_length=5, max_length=500)
    phone: str | None = None
    cuisine_type: str | None = None
    is_open: bool | None = None
    delivery_fee: float | None = Field(default=None, ge=0)
    minimum_order: float | None = Field(default=None, ge=0)
    
    
class RestaurantOut(BaseModel):
    id:uuid.UUID
    owner_id:uuid.UUID
    name:str
    description:str|None
    address:str
    phone:str
    is_open:bool
    image:str|None
    cuisine_type:str|None
    rating:float
    delivery_fee:float
    
    model_config={"from_attributes":True}