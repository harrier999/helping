from chromadb import QueryResult
import openai
import core.chroma
from settings import settings
from core import chatting


openai.api_key = settings.API_KEY

class ChatBot:
    def __init__(self):
        self.prompt = """
        
        """
        self.client = core.chroma.get_client()
        self.collection = self.client.get_collection(settings.COLLECTION_NAME)

    def get_response(self, chatting_room: chatting.ChattingRoom):
        question = str(chatting_room.get_last_user_chat())
        answers: QueryResult = self._get_nearest_questions(question)
        chatting_room.add_chat(chatting.SystemChat("다음 Q&A 정보를 참고해서 사용자의 질문에 답변해주세요."))
        for question, document in zip(answers["ids"][0], answers["documents"][0]):
            chatting_room.chats.append(chatting.SystemChat(f"질문: {question} 답변: {document}"))
        
        response = openai.chat.completions.create(
            model=settings.CHAT_MODEL, messages=chatting_room.get_chats()
        )
        return response.choices[0].message.content
    
    
    def _get_nearest_questions(self, question, k=10) -> QueryResult:
        question_embeding = openai.embeddings.create(input=[question], model=settings.EMBEDING_MODEL).data[0].embedding
        return self.collection.query(query_embeddings=[question_embeding], n_results=k)
        
        