import os

import pandas as pd
import chromadb
import uuid
import re
from logging_config import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
csv_file_path = os.getenv('CSV_FILE_PATH')
collection_name = os.getenv('CHROMA_COLLECTION_NAME')
max_result = os.getenv('MAX_RESULT')

class Portfolio:

    def __init__(self, file_path=csv_file_path):
        # Load the .csv template into a dataframe
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)
        # Create ChromaDB persistent client and collection
        self.chroma_client = chromadb.PersistentClient(collection_name)
        self.existing_collections = self.chroma_client.list_collections()
        # Check if collection exists
        self.collection_exists = any(
            collection.name == collection_name
            for collection in self.existing_collections
        )
        # if exists delete collection, else ignore
        if self.collection_exists:
            self.chroma_client.delete_collection(name=collection_name)
            logger.info(f"Collection '{collection_name}' has been deleted.")
        else:
            logger.info(f"Collection '{collection_name}' does not exist.")

        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)


    def populate_chroma_collection(self):
        # Add data from CSV to ChromaDB collection if it's empty
        if not self.collection.count():
            for _, row in self.df.iterrows():
                self.collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )


    def query_chroma_collection(self, technical_skills, max_results=int(max_result)):
        # Query ChromaDB collection using technical skills from JSON response
        num_elements = self.collection.count()
        n_results = min(max_results, num_elements)
        result = self.collection.query(
            query_texts=technical_skills,
            n_results=n_results
        )
        return result


if __name__ == "__main__":
    print(os.getenv("CSV_FILE_PATH"))
