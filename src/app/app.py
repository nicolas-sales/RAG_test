from fastapi import FastAPI

from src.app.routes import router

app = FastAPI(
    title="France Mutuelle Internal Chatbot",
    version="1.0.0"
)

app.include_router(router)