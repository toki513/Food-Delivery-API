from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self,status_code:int,detail:str):
        self.status_code=status_code
        self.detail=detail
        super().__init__(detail)
        
class NotFoundException(AppException):
    def __init__(self,resource:str = "Resource"):
        super().__init__(
            status_code=404,
            detail=f"{resource} not found"
        )
class UnauthorizedException(AppException):
    def __init__(self,detail:str="Not authorized"):
        super().__init__(status_code=404,detail=detail)

class ForbiddenException(AppException):
    def __init__(self,detail:str="Access Forbidden"):
        super().__init__(status_code=403, detail=detail)
        
class BadRequestException(AppException):
    def __init__(self,detail:str):
        super().__init__(status_code=400,detail=detail)
        
class ConflictException(AppException):
    def __init__(self,detail:str):
        super().__init__(status_code=409,detail=detail)
        
def register_exception_handlers(app:FastAPI)->None:
    @app.exception_handler(AppException)
    async def handle_app_exception(
        request:Request,
        exc:AppException
    )->JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail":exc.detail}
        )