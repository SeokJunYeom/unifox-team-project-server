# -*- coding: utf-8 -*-

from socket import *
from select import *
import sys
from time import ctime

Host = ''
PORT = 56789
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 생성
# socket(socket_family, socket_type, protocoal = 0)
serverSocket = socket(AF_INET, SOCK_STREAM)

# 주소와 포트 할당
serverSocket.bind(ADDR)

# 요청을 기다림
# 10개의 클라이언트 대기 가능
serverSocket.listen(10)
connection_list = [serverSocket]
print("채팅 서버 시작")
