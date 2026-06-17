from fastapi import FastAPI
from pydantic import BaseModel

from src.pipeline.rag_pipeline import RAGPipeline

app = FastAPI(
    title="France Mutuelle Internal Chatbot",
    version="1.0.0"
)

rag_pipeline = RAGPipeline()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "France Mutuelle RAG API"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = rag_pipeline.ask(
        request.question
    )

    return result