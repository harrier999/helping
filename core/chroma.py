import chromadb
import logging


def get_client() -> chromadb.ClientAPI:
    logging.info("Connecting to ChromaDB")
    chroma_client = chromadb.HttpClient(
        host="http://localhost:8000",
        ssl=False,
        headers=None,
        settings=chromadb.config.Settings(),
        database=chromadb.config.DEFAULT_DATABASE,
    )
    logging.info("Connected to ChromaDB")
    return chroma_client


# def get_client() -> chromadb.ClientAPI:
#     logging.info("Connecting to ChromaDB")
#     chroma_client = chromadb.PersistentClient(
#         host="http://chromadb",
#         port=8000,
#         ssl=False,
#         headers=None,
#         settings=chromadb.config.Settings(),
#         database=chromadb.config.DEFAULT_DATABASE,
#     )
#     logging.info("Connected to ChromaDB")
#     return chroma_client