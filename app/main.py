from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine
from app.api.users import router as users_router
from app.api.candidates import router as candidates_router

app = FastAPI()

app.include_router(users_router)
app.include_router(candidates_router)



@app.get("/health")
def health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": result.scalar(),
        }