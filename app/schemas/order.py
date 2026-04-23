import uuid
from pydantic import BaseModel, Field
from app.models.order import OrderStatus, PaymentStatus


class OrderItemCreate(BaseModel):
    menu_item_id: uuid.UUID
    quantity: int = Field(ge=1, le=100)
    special_instructions: str | None = None


class OrderCreate(BaseModel):
    restaurant_id: uuid.UUID
    items: list[OrderItemCreate] = Field(min_length=1)
    delivery_address: str = Field(min_length=5, max_length=500)
    special_instructions: str | None = None


class OrderItemOut(BaseModel):
    id: uuid.UUID
    menu_item_id: uuid.UUID | None
    quantity: int
    price_at_time: float
    name_at_time: str
    special_instructions: str | None

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID | None
    restaurant_id: uuid.UUID | None
    rider_id: uuid.UUID | None
    status: OrderStatus
    payment_status: PaymentStatus
    total_amount: float
    delivery_fee: float
    delivery_address: str
    special_instructions: str | None
    estimated_delivery_time: int | None
    items: list[OrderItemOut]

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderRiderAssign(BaseModel):
    rider_id: uuid.UUID