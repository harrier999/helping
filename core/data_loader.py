import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pickle
import logging

import chromadb
import openai
from chromadb.utils.embedding_functions import openai_embedding_function
from chroma import get_client
from settings import settings

logging.basicConfig(level=logging.INFO)

API_KEY = settings.API_KEY
MODEL = settings.EMBEDING_MODEL
METADATA = settings.CHROMA_METADATA
openai.api_key = API_KEY

METADATA={"hnsw:space":"l2"}

class DataLoader:
    collection_name = settings.COLLECTION_NAME
    
    def __init__(self, chroma_client: chromadb.ClientAPI):
        self.client = chroma_client
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except Exception as e:
            self.collection = self.client.create_collection(self.collection_name, metadata=METADATA)

    def save_data(self, data: dict):
        """
        데이터를 데이터베이스에 저장합니다.
        """
        embedding_function = openai_embedding_function.OpenAIEmbeddingFunction(api_key=API_KEY, model_name=MODEL)
        self.collection = self.client.create_collection(self.collection_name, metadata=METADATA, embedding_function=embedding_function)
        
        questions = data.keys()
        answers = data.values()
        
        resp = openai.embeddings.create(input=list(questions)[:2000], model=MODEL)
        embeddings = [embedding.embedding for embedding in resp.data]
        
        self.collection.add(
            ids=list(questions)[:2000],
            embeddings=embeddings,
            documents=list(answers)[:2000],
        )
        
        resp = openai.embeddings.create(input=list(questions)[2000:], model=MODEL)
        embeddings = [embedding.embedding for embedding in resp.data]
        
        self.collection.add(
            ids=list(questions)[2000:],
            embeddings=embeddings,
            documents=list(answers)[2000:],
        )
        
        logging.info("Data is saved to ChromaDB.")

    def delete_data(self):
        """
        데이터베이스의 데이터를 삭제합니다.
        """
        self.client.delete_collection(self.collection_name)
        
    def load_data_from_pkl(self, path):
        """
        pkl 파일에서 데이터를 로드합니다.
        """
        with open(path, 'rb') as f:
            data = pickle.load(f)
        return data

if __name__ == "__main__":
    data_loader = DataLoader(chroma_client=get_client())

    logging.info("Deleting data from ChromaDB...")
    data_loader.delete_data()
    
    logging.info("Loading data from pkl file...")
    data = data_loader.load_data_from_pkl('core/data/refined_data.pkl')
    
    logging.info("Saving data to ChromaDB...")
    data_loader.save_data(data)
    
    logging.info("Data loading is done.")