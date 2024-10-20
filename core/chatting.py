class Chat:
    def __init__(self, text):
        self.text = text
        
    def __str__(self):
        return self.text


class UserChat(Chat):
    def __init__(self, text):
        super().__init__(text)
        
    @property
    def data(self):
        return {"role": "user", "type": "text", "content": self.text}
    
    
class BotChat(Chat):
    def __init__(self, text):
        super().__init__(text)
        
    @property
    def data(self):
        return {"role": "assistant", "type": "text", "content": self.text}
    
class SystemChat(Chat):
    def __init__(self, text):
        super().__init__(text)
        
    @property
    def data(self):
        return {"role": "system", "type": "text", "content": self.text}
        
class ChattingRoom:
    prompt = """
    당신은 네이버 스마트스토어 상담사 역할을 하는 챗봇입니다.
    사용자는 네이버 쇼핑에 관한 여러가지 질문을 할 예정입니다.
    사용자가 질문을하면, 이와 관련된 Q&A 정보가 제공됩니다. 제공된 정보를 바탕으로 사용자의 질문에 답변해주세요.
    네이버 스마트스토어 관련되지 않은 질문에는 반드시 '저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다' 라고 답해주세요.
    만약 Q&A 정보가 없다면, 반드시 '죄송합니다. 제가 알지 못하는 질문입니다..' 라고 답해주세요.
    절대로 거짓 정보나 틀린 정보를 제공해서는 안됩니다.
    '안녕하세요' 와 같은 인사에는 '안녕하세요 스마트 스토어에 대한 질문이 있으신가요?' 라고 답해주세요.
    최대한 성의있고 친절하게 네이버 스마트스토어 상담사 역할을 해주세요
    사용자가 Q&A에 없는 질문을 하면, 질문과 연관 없는 Q&A가 제공될 수 있습니다. 네이버 스마트스토어에 관련된 질문이라면, 기존 대화내용 참고하여 답변해주세요.
    여전히 답변이 어렵다면, '죄송합니다. 제가 알지 못하는 질문입니다' 라고 답해주세요. 절대 틀린 내용을 제공해서는 안됩니다.
    
    """
    def __init__(self):
        self.chats: list[Chat] = []

        self.add_chat(SystemChat(self.prompt))
        
    def add_chat(self, chat: Chat):
        self.chats.append(chat)
        
    def get_chats(self):
        return [chat.data for chat in self.chats]
    
    def get_last_user_chat(self):
        for chat in reversed(self.chats):
            if isinstance(chat, UserChat):
                return chat
        return None
            
    def __str__(self):
        return str([str(chat) for chat in self.chats])
        
