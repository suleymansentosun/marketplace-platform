from fastapi import FastAPI
from routers import advertisement, category
from db import models
from db.database import engine

app = FastAPI()
app.include_router(advertisement.router)
app.include_router(category.router)

models.Base.metadata.create_all(engine)