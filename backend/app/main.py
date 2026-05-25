from fastapi import FastAPI
from app.database.connection import database
from app.routes.auth_router import router as auth_router
from app.routes.chat_router import router as chat_router
from app.routes.example import router as example_router
from app.routes.user_router import router as user_router

app = FastAPI(
    title="TEAcolhe Backend",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(example_router)
app.include_router(user_router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()