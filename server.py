# -*- coding: utf-8 -*-

from socket import *
from select import *
from time import ctime
import os, sys
import imgProcess
 
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

def dir():
	string = ""

	for root, dirs, files in os.walk("image/"):
		for file in files:
			string += file + ","

	print(string)

	return string

def revall(buf, sock, count):	
	while count:
		newbuf = sock.recv(count)
		
		if not newbuf:
			return None

		buf += newbuf
		count -= len(newbuf)
	
	return buf

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
				try:
					data = sock.recv(BUFSIZE)

					if data:
						print("[%s] 클라이언트로부터 데이터를 전달 받음." % ctime())

					else:
						print("[%] 클라이언트와 연결 끊김." % ctime())
						connection_list.remove(sock)
						sock.close()

					head = data.split("*")[0]

					if head == "image":
						print("[%s] 클라이언트로부터 이미지 데이터를 받는 중." % ctime())

						imgName = data.split("*")[1]
						imgLen = data.split("*")[2]
						imgData = data[int(len(imgLen)) + int(len(imgName)) + 8:]

						imgData = revall(imgData, sock, int(imgLen) - len(imgData))
						imgProcess.imgSave(imgName, imgProcess.imgDecode(imgData))

						print("[%s] 클라이언트로부터 이미지 전달 받음." % ctime())

					if head == "request":
						if data.split("*")[1] == "dir":
							sock.send(dir())
							print("[%s] 클라이언트에 image/ 디렉토리 목록 넘겨줌." % ctime())

						else:
							imgStr = imgProcess.imgToString(data.split("*")[1])
							sock.send(imgStr)
							print("[%s] 클라이언트에 이미지 전달." % ctime())

				except:
					print("[%s] 클라이언트와 연결 끊김." % ctime())
					connection_list.remove(sock)
					sock.close()

	except KeyboardInterrupt:
		serverSocket.close()
		sys.exit()

