from fastapi import FastAPI, Depends
from api.controller.person_controller import router as people_router

from db import get_db

app = FastAPI()

app.include_router(people_router)

@app.get("/")
def home():
    return {"message": "Hello, UniCaf!"}

@app.get("/version")
def db_version(conn=Depends(get_db)):
    version = conn.execute("SELECT version()").fetchone()
    return {"postgres_version": version}
