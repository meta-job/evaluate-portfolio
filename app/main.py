from fastapi import FastAPI
from .routers import portfolio
from .routers import user
import logging

app = FastAPI()

app.include_router(portfolio.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"Hello": "World"}