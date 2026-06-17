import sys

from langchain_openai import OpenAIEmbeddings

from src.utils.logger import logging
from src.utils.exception import CustomException


class EmbeddingModel:

    def __init__(
        self,
        model_name="text-embedding-3-small"
    ):

        self.model_name = model_name

    def load_embeddings(self):

        try:

            logging.info(
                f"Loading embedding model {self.model_name}"
            )

            embeddings = OpenAIEmbeddings(
                model_name=self.model_name
            )

            logging.info(
                "Embedding model loaded successfully"
            )

            return embeddings

        except Exception as e:
            raise CustomException(e, sys)