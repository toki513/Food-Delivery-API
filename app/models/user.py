import uuid
import enum 
from sqlalchemy import String, Boolean, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base



class UserRole(str,enum.Enum):
        CUSTOMER="customer"
        RESTAURANT_OWNER="restaurant_owner"
        RIDER="rider"
        ADMIN="admin"
        

class User(Base):
    __tablename__="users"
    
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email:Mapped[str]=mapped_column(String,unique=True,index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password:Mapped[str]=mapped_column(String(255))
    
    role:Mapped[UserRole]=mapped_column(
        SAEnum(UserRole),
        default=UserRole.CUSTOMER,
        nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    profile_image: Mapped[str | None] = mapped_column(String(500), nullable=True)


    restaurants:Mapped[list["Restaurant"]]=relationship(
        "Restaurant",back_populates="owner",lazy="selectin"
    )
    
    orders:Mapped[list["Order"]]=relationship(
        "Order",back_populates="customer", foreign_keys="Order.customer_id",lazy="selectin"
        )
    
    deliveries:Mapped[list["Order"]]=relationship(
        "Order",back_populates="rider",foreign_keys="Order.rider_id",lazy="selectin"
    )
    
    def __repr__(self) ->str:
          return f"<User {self.email} ({self.role})>"