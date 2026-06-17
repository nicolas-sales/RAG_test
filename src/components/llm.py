import sys

from langchain_openai import ChatOpenAI

from src.utils.logger import logging
from src.utils.exception import CustomException


class LLM:
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0,
    ):
        self.model_name = model_name
        self.temperature = temperature

    def load_llm(self):
        try:
            logging.info(f"Loading LLM: {self.model_name}")

            llm = ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
            )

            logging.info("LLM loaded successfully")
            return llm

        except Exception as e:
            raise CustomException(e, sys)