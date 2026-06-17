from fastapi import APIRouter

from src.pipelines.rag_pipeline import RAGPipeline
from src.app.schemas import QuestionRequest

router = APIRouter()

rag_pipeline = RAGPipeline()


@router.get("/")
def home():

    return {
        "message": "France Mutuelle RAG API"
    }


@router.post("/ask")
def ask_question(request: QuestionRequest):

    return rag_pipeline.ask(
        request.question
    )