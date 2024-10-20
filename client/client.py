import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from settings import settings
import websocket
import threading
import time

# 웹소켓 서버 URL
WEBSOCKET_URL = f"ws://localhost:{settings.SERVER_PORT}/ws"  # 여기에 실제 웹소켓 서버 URL을 입력하세요.

# 메시지를 수신하는 콜백 함수
def on_message(ws, message):
    print(f"\n상담사: {message}")  # 수신한 메시지를 출력
    print("\n")
    global waiting_for_response
    waiting_for_response = False  # 응답을 받았으므로 대기 상태 해제

# 웹소켓 연결이 열릴 때 호출되는 콜백 함수
def on_open(ws):
    def run(*args):
        global waiting_for_response
        while True:
            message = input("사용자: ")  # 사용자 입력 받기
            waiting_for_response = True  # 응답 대기 상태로 설정
            ws.send(message)  # 메시지 전송

            # 응답을 기다리는 동안 대기
            while waiting_for_response:
                time.sleep(0.1)  # CPU 사용량을 줄이기 위한 소량의 대기

    threading.Thread(target=run).start()  # 입력을 위한 스레드 시작

# 웹소켓 연결이 닫힐 때 호출되는 콜백 함수
def on_close(ws, a, b):
    ws.close()
    print("Connection closed")
    exit()

# 웹소켓 에러 발생 시 호출되는 콜백 함수
def on_error(ws, error):
    ws.close()
    print("Error:", error)
    exit()

# 전역 변수로 응답 대기 상태를 관리
waiting_for_response = False

# 웹소켓 클라이언트 생성 및 실행
if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=on_message,
        on_open=on_open,
        on_close=on_close,
        on_error=on_error
    )

    # 웹소켓 연결 시작
    ws.run_forever()
