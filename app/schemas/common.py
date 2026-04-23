from pydantic import BaseModel
from typing import Generic, TypeVar, List

T=TypeVar("T")

class PaginationParams(BaseModel):
    page:int=1
    page_size:int=20
    
    @property
    def offset(self) ->int:
        return (self.page - 1) * self.page_size
    
    class Config:
        model_config={"from_attributes":True}
        
class PaginatedResponse(BaseModel,Generic[T]):
    items:List[T]
    total:int
    page:int
    page_size:int
    total_pages:int
    
    @classmethod
    def create(cls,items:List[T],total:int,page:int,page_size:int):
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total+page_size - 1)//page_size,
        )

class MessageResponse(BaseModel):
    message:str
    