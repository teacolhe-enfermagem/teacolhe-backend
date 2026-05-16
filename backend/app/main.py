from fastapi import FastAPI
from app.database.connection import database
from app.routes.auth_router import router as auth_router

app = FastAPI(
    title="TEAcolhe Backend",
    version="1.0.0"
)

app.include_router(auth_router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()