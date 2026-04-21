from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.api.v1.router import api_router


def create_application()->FastAPI:
    application=FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        debug=settings.DEBUG
    )
        
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    application.mount(
        "/uploads",
        StaticFiles(directory=settings.UPLOAD_DIR),
        name="uploads"
    )

    application.include_router(api_router,prefix=settings.API_V1_STR)


    register_exception_handlers(application)
    
    return application




app=create_application()




@app.get("/health", tags=["health"])
async def health_check():
    return{
        "status ":"Healthy",
        "app":settings.APP_NAME
    }