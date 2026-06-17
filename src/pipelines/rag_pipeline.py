from pathlib import Path
import sys

from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.components.embeddings import EmbeddingModel
from src.components.vector_store import VectorStore
from src.components.retriever import Retriever
from src.components.llm import LLM
from src.components.prompt import PromptTemplate

from src.utils.logger import logging
from src.utils.exception import CustomException


class RAGPipeline:
    def __init__(self):
        load_dotenv()

        self.project_root = Path(__file__).resolve().parents[2]
        self.vector_store_path = self.project_root / "vector_store"

        self.embeddings = None
        self.vector_store = None
        self.retriever = None
        self.llm = None
        self.prompt = None
        self.rag_chain = None

        self._build_pipeline()

    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def _build_pipeline(self):
        try:
            logging.info("Building RAG pipeline")

            embedding_model = EmbeddingModel()
            self.embeddings = embedding_model.load_embeddings()

            vector_store_component = VectorStore(
                persist_directory=self.vector_store_path
            )
            self.vector_store = vector_store_component.load_vector_store(
                embeddings=self.embeddings
            )

            retriever_component = Retriever(
                search_type="mmr",
                k=4,
            )
            self.retriever = retriever_component.get_retriever(
                self.vector_store
            )

            llm_component = LLM()
            self.llm = llm_component.load_llm()

            prompt_component = PromptTemplate()
            self.prompt = prompt_component.get_prompt()

            self.rag_chain = (
                {
                    "context": self.retriever | self._format_docs,
                    "question": RunnablePassthrough(),
                }
                | self.prompt
                | self.llm
                | StrOutputParser()
            )

            logging.info("RAG pipeline built successfully")

        except Exception as e:
            raise CustomException(e, sys)

    def ask(self, question: str):

        try:

            logging.info(f"User question: {question}")

            docs = self.retriever.invoke(question)

            answer = self.rag_chain.invoke(question)

            sources = []

            for doc in docs:

                sources.append(
                    {
                        "file": doc.metadata.get("source", "Unknown"),
                        "section": doc.metadata.get("h2"),
                        "type": doc.metadata.get(
                            "document_type",
                            "Unknown"
                        ),
                    }
                )

            unique_sources = []

            seen = set()

            for source in sources:

                key = (
                    source["file"],
                    source["section"]
                )

                if key not in seen:

                    seen.add(key)

                    unique_sources.append(source)

            result = {
                "question": question,
                "answer": answer,
                "sources": unique_sources
            }

            logging.info(
                f"Answer generated successfully"
            )

            return result

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    rag = RAGPipeline()

    questions = [
        "Comment se déroule la gestion des réclamations ?",
        "Comment obtenir un token ?",
        "Retrait bloqué depuis 5 jours",
        "Quelle est la météo à Paris ?",
    ]

    for question in questions:
        result = rag.ask(question) 

        print("=" * 100)
        print(f"Question : {result['question']}")
        print()
        print(result["answer"])
        print()
        print(f"Sources : {result['sources']}")