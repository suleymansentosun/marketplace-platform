from fastapi import FastAPI
from routers import advertisement, category, conversation, message, payment_proposal, user, reviews
from db import models
from db.database import engine
from auth import authentication


app = FastAPI()
app.include_router(reviews.router)
app.include_router(authentication.router)
app.include_router(advertisement.router)
app.include_router(category.router)
app.include_router(payment_proposal.router)
app.include_router(user.router)
app.include_router(conversation.router)
app.include_router(message.router)

models.Base.metadata.create_all(engine)