import socket
from threading import Thread

def recv_message(sock):
    while True:
        msg = sock.recv(1024) # 1024 바이트 데이터 수신
        print(msg.decode())

# AF_INET : IPv4 사용, SOCK_STREAM : TCP 패킷 수신
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8888))

th = Thread(target=recv_message, args=(sock,))
th.daemon = True
th.start()

while True:
    msg = input()
    sock.send(msg.encode())
    if msg == '/종료':
        break

sock.close()