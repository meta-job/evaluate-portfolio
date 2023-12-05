from fastapi import FastAPI
from .routers import resume
from .routers import user
import logging

app = FastAPI()

app.include_router(resume.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"Hello": "World"}