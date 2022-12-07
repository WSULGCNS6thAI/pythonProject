from socket import *
import threading
import time

# 메시지 전송 함수
def send(sock):
    while True:
        sendData = input('>>>')
        sock.send(sendData.encode('utf-8'))

# 메시지 수신 함수
def receive(sock):
    while True:
        recvData = sock.recv(1024) # 1024 바이트 데이터 수신
        print('상대방 :', recvData.decode('utf-8'))

port = 8081

# AF_INET : IPv4 사용
# SOCK_STREAM : tcp 패킷 수신
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1) # n개 클라이언트 접속 허용

print('%d번 포트로 접속 대기중...'%port)

connectionSock, addr = serverSock.accept()

print(str(addr), '에서 접속되었습니다.')

# 쓰레드 생성
sender = threading.Thread(target=send, args=(connectionSock,))
receiver = threading.Thread(target=receive, args=(connectionSock,)) 

sender.start()
receiver.start()

# 무한 루프
while True: 
    time.sleep(1) # 1초 대기 
    pass