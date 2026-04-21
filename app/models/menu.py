import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Boolean,String,ForeignKey,Text,Integer,Float
from app.db.base import Base

class MenuItem(Base):
    __tablename__="menu_items"
    
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True)
    
    restaurant_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("restaurants.id",ondelete="CASCADE"),index=True,nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    preparation_time: Mapped[int] = mapped_column(Integer, default=15) 
    calories: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    
    restaurant:Mapped["Restaurant"]=relationship(
        "Restaurant", back_populates="menu_items"
    )
    
    order_items:Mapped[list["Order"]]=relationship(
        "Order",back_populates="menu_item",lazy="selectin"
    )
    