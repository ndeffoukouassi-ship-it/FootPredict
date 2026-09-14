from fastapi import APIRouter
from app.api.v1 import matches, predictions

api_router = APIRouter()
api_router.include_router(matches.router, prefix="/matches", tags=["Matches"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
