from fastapi import FastAPI
from routers import advertisement, category, transaction, user, reviews
from db import models
from db.database import engine
from auth import authentication


app = FastAPI()
app.include_router(reviews.router)
app.include_router(authentication.router)
app.include_router(advertisement.router)
app.include_router(category.router)
app.include_router(transaction.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)