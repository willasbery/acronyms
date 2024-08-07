from fastapi import FastAPI
from .routes.acronyms import router as acronyms_router

app = FastAPI()

app.include_router(acronyms_router, prefix="/acronyms", tags=["acronyms"])
