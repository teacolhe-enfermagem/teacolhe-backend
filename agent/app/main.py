from fastapi import FastAPI
from app.routes.chat_router import router as chat_router

app = FastAPI(
    title="TEAcolhe Agent",
    version="1.0.0"
)

app.include_router(chat_router)

