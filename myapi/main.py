from fastapi import FastAPI
from myapi.routers import router
import uvicorn

from myapi.db import create_db_and_tables

from myapi.models import (
    Usuario,
)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(router=router)








            