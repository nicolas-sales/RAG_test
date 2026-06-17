from pathlib import Path
import sys

from dotenv import load_dotenv

from src.components.document_loader import DocumentLoader
from src.components.embeddings import EmbeddingModel
from src.components.vector_store import VectorStore

from src.utils.logger import logging
from src.utils.exception import CustomException


class IngestionPipeline:
    def __init__(self):
        load_dotenv()

        self.project_root = Path(__file__).resolve().parents[2]
        self.data_path = self.project_root / "data"
        self.ticket_file = self.data_path / "corpus_tickets_support.json"
        self.vector_store_path = self.project_root / "vector_store"

    def run(self):
        try:
            logging.info("Starting ingestion pipeline")

            loader = DocumentLoader()

            documents = loader.load_documents(
                data_path=self.data_path,
                ticket_file=self.ticket_file,
            )

            embedding_model = EmbeddingModel()
            embeddings = embedding_model.load_embeddings()

            vector_store_component = VectorStore(
                persist_directory=self.vector_store_path
            )

            vector_store = vector_store_component.create_vector_store(
                documents=documents,
                embeddings=embeddings,
            )

            logging.info("Ingestion pipeline completed successfully")

            return vector_store

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()

    print("Ingestion terminée avec succès.")