from fastapi import APIRouter

from app.api.v1.endpoints import(
    auth,
    users,
    restaurants,
    menus,
    orders,
)

api_router=APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)
api_router.include_router(
    restaurants.router,
    prefix="/restaurants",
    tags=["Restaurants"]
)

api_router.include_router(
    menus.router,
    prefix="/menus",
    tags=["Menus"]
)

api_router.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"]
)