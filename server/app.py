import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import logging
from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
from settings import settings
from core import chatbot, chatting

logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    chatting_room = chatting.ChattingRoom()
    chat_bot = chatbot.ChatBot()
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(data)
            chatting_room.add_chat(chatting.UserChat(data))
            response = chat_bot.get_response(chatting_room)
            logging.info(response)
            chatting_room.add_chat(chatting.BotChat(response))
            await websocket.send_text(f"{response}")
    except WebSocketDisconnect:
        logging.warn("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVER_PORT)