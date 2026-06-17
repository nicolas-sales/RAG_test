from pathlib import Path
import sys

from langchain_chroma import Chroma

from src.utils.logger import logging
from src.utils.exception import CustomException


class VectorStore:
    def __init__(self, persist_directory):
        self.persist_directory = Path(persist_directory)

    def create_vector_store(self, documents, embeddings):
        try:
            logging.info("Creating Chroma vector store")

            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=str(self.persist_directory),
            )

            logging.info(
                f"Vector store created at: {self.persist_directory}"
            )

            return vector_store

        except Exception as e:
            raise CustomException(e, sys)

    def load_vector_store(self, embeddings):
        try:
            logging.info(
                f"Loading Chroma vector store from: {self.persist_directory}"
            )

            vector_store = Chroma(
                persist_directory=str(self.persist_directory),
                embedding_function=embeddings,
            )

            logging.info("Vector store loaded successfully")
            return vector_store

        except Exception as e:
            raise CustomException(e, sys)