import os

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")
EMBEDING_MODEL =  "text-embedding-3-large"
CHAT_MODEL = "gpt-4o"
CHROMA_METADATA = {"hnsw:space":"l2"}

COLLECTION_NAME = "naver_shopping"

SERVER_PORT = 8888
