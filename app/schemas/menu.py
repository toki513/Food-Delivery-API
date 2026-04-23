import uuid
from pydantic import BaseModel, Field


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str | None = None
    price: float = Field(gt=0)  # gt=0 means must be greater than 0
    category: str | None = Field(default=None, max_length=100)
    preparation_time: int = Field(default=15, ge=1, le=120)
    calories: int | None = Field(default=None, ge=0)


class MenuItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    category: str | None = None
    is_available: bool | None = None
    preparation_time: int | None = Field(default=None, ge=1, le=120)
    calories: int | None = None


class MenuItemOut(BaseModel):
    id: uuid.UUID
    restaurant_id: uuid.UUID
    name: str
    description: str | None
    price: float
    category: str | None
    image: str | None
    is_available: bool
    preparation_time: int
    calories: int | None

    model_config = {"from_attributes": True}