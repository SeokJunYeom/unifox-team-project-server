# -*- coding: utf-8 -*-

from socket import *
from select import *
import sys
from time import ctime

HOST = ''
PORT = 50010
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
print("서버 시작")

while connection_list:
	try:
		print("요청 대기")

		# select로 요청 받고 10초마다 블럭킹 해제
		read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

		for sock in read_socket:
			if sock == serverSocket:
				clientSocket, addr_info = serverSocket.accept()
				connection_list.append(clientSocket)
				print("[%s] 클라이언트(%s) 연결 성공." % (ctime(), addr_info[0]))

			else:
				data = sock.recv(BUFSIZE)
				if data:
					print("[%s] 클라이언트로부터 데이터를 전달 받음." % ctime())
					print("받은 데이터 : %s" % data)

				else:
					print("[%s] 클라이언트 (%s) 와 연결 끊김." % (ctime(), sock))
					connection_list.remove(sock)
					sock.close()

	except KeyboardInterrupt:
		serverSocket.close()
		sys.exit()
