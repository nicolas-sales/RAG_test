from pathlib import Path
import json
import sys

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

from src.utils.logger import logging
from src.utils.exception import CustomException


class DocumentLoader:

    def __init__(self):

        self.headers_to_split_on = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ]

        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on
        )

    def load_markdown_documents(self, data_path):

        try:

            data_path = Path(data_path)

            documents = []

            for md_file in data_path.glob("*.md"):

                logging.info(f"Loading markdown file : {md_file.name}")

                with open(md_file, "r", encoding="utf-8") as f:
                    text = f.read()

                md_docs = self.markdown_splitter.split_text(text)

                for doc in md_docs:

                    doc.metadata["source"] = md_file.name
                    doc.metadata["document_type"] = "markdown"

                documents.extend(md_docs)

            logging.info(
                f"Loaded {len(documents)} markdown documents"
            )

            return documents

        except Exception as e:
            raise CustomException(e, sys)

    def load_ticket_documents(self, json_file):

        try:

            json_file = Path(json_file)

            logging.info(
                f"Loading ticket file : {json_file.name}"
            )

            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            documents = []

            for ticket in data["tickets"]:

                content = f"""
ID : {ticket.get('id')}
Date : {ticket.get('date')}
Catégorie : {ticket.get('category')}
Statut : {ticket.get('status')}
Priorité : {ticket.get('priority')}

Sujet :
{ticket.get('subject')}

Description :
{ticket.get('description')}

Résolution :
{ticket.get('resolution')}

Agent :
{ticket.get('agent')}

Durée :
{ticket.get('duration_hours')} heures
"""

                documents.append(
                    Document(
                        page_content=content.strip(),
                        metadata={
                            "source": json_file.name,
                            "document_type": "ticket",
                            "ticket_id": ticket.get("id")
                        }
                    )
                )

            logging.info(
                f"Loaded {len(documents)} tickets"
            )

            return documents

        except Exception as e:
            raise CustomException(e, sys)

    def load_documents(self, data_path, ticket_file):

        try:

            markdown_docs = self.load_markdown_documents(
                data_path
            )

            ticket_docs = self.load_ticket_documents(
                ticket_file
            )

            documents = markdown_docs + ticket_docs

            logging.info(
                f"Total documents loaded : {len(documents)}"
            )

            return documents

        except Exception as e:
            raise CustomException(e, sys)
        


if __name__=="__main__":

    loader = DocumentLoader()

    docs = loader.load_documents(
        data_path="data",
        ticket_file="data/corpus_tickets_support.json"
    )

    print(f"\nNombre total de documents : {len(docs)}")

    print("\nPremier document")
    print("=" * 100)

    print(docs[0].page_content[:1000])

    print("\nMetadata")
    print("=" * 100)

    print(docs[0].metadata)

    ticket_docs = [
    doc
    for doc in docs
    if doc.metadata["document_type"] == "ticket"
    ]

    print(f"\nNombre de tickets : {len(ticket_docs)}")

    print(ticket_docs[0].page_content)
