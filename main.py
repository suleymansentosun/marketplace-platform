from fastapi import FastAPI
from routers import advertisement, category, transaction
from db import models
from db.database import engine

app = FastAPI()
app.include_router(advertisement.router)
app.include_router(category.router)
app.include_router(transaction.router)

models.Base.metadata.create_all(engine)