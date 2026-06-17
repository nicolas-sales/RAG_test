import sys

from src.utils.logger import logging
from src.utils.exception import CustomException


class Retriever:
    def __init__(self, search_type: str = "mmr", k: int = 4):
        self.search_type = search_type
        self.k = k

    def get_retriever(self, vector_store):
        try:
            logging.info(
                f"Creating retriever with search_type={self.search_type}, k={self.k}"
            )

            retriever = vector_store.as_retriever(
                search_type=self.search_type,
                search_kwargs={"k": self.k},
            )

            logging.info("Retriever created successfully")
            return retriever

        except Exception as e:
            raise CustomException(e, sys)