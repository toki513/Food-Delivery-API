import uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Boolean,Float,ForeignKey,Text
from app.db.base import Base


class Restaurant(Base):
    __tablename__="restaurants"
    
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True)

    owner_id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False,index=True)
    
    address:Mapped[str]=mapped_column(String(255))
    name:Mapped[str]=mapped_column(String(255),nullable=False,index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cuisine_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_open:Mapped[bool]=mapped_column(Boolean,default=True)
    rating:Mapped[float]=mapped_column(Float,default=0.0)
    delivery_fee:Mapped[float]=mapped_column(Float,default=0.0)
    minimum_order: Mapped[float] = mapped_column(Float, default=0.0)
    
    owner:Mapped["User"]=relationship(
        "User",back_populates="restaurants"
    )
    
    menu_items:Mapped[list["MenuItem"]]=relationship(
        "MenuItem",back_populates="restaurant",cascade="all,delete-orphan",lazy="selectin"
    )
    
    