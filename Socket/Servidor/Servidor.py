# import socket
# import os
# import signal
# import sys

# HOST = '192.168.2.5'
# PORT = 7777
# BUFFER_SIZE = 1024
# VIDEOS_DIR = "videos"

# # Handler para capturar o Ctrl+C
# def signal_handler(sig, frame):
#     print("\nEncerrando o servidor.")
#     sys.exit(0)

# # Configura o handler para o sinal SIGINT (Ctrl+C)
# signal.signal(signal.SIGINT, signal_handler)

# if not os.path.exists(VIDEOS_DIR):
#     os.makedirs(VIDEOS_DIR)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     s.settimeout(2)  # Define um timeout de 2 segundos

#     print("Servidor escutando...")

#     while True:  # Mantém o servidor sempre escutando por novas conexões
#         try:
#             conn, addr = s.accept()
#             with conn:
#                 print('Conectado por', addr)
#                 conn.settimeout(2)  # Também define um timeout para a conexão com o cliente

#                 while True:
#                     try:
#                         data = conn.recv(BUFFER_SIZE)
#                         if not data:
#                             break

#                         cmd, filename = data.decode().split(',')

#                         if cmd == 'upload':
#                             with open(os.path.join(VIDEOS_DIR, filename), 'wb') as f:
#                                 while True:
#                                     file_data = conn.recv(BUFFER_SIZE)
#                                     if file_data == b'DONE':
#                                         break
#                                     f.write(file_data)

#                             print(f"{filename} uploaded successfully!")

#                         elif cmd == 'list':
#                             files = os.listdir(VIDEOS_DIR)
#                             conn.send(','.join(files).encode())

#                         elif cmd == 'download':
#                             with open(os.path.join(VIDEOS_DIR, filename), 'rb') as f:
#                                 for line in f:
#                                     conn.send(line)

#                             print(f"{filename} sent successfully!")
#                     except socket.timeout:
#                         continue

#         except socket.timeout:
#             continue



##########################################################################################################################################################################


# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = 'localhost'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('ESCUTANDO EM:',socket_address)

vid = cv2.VideoCapture('video1.mp4') #  replace 'rocket.mp4' with 0 for webcam
fps,st,frames_to_count,cnt = (0,0,20,0)

while True:
	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	print('Conexão recebida de ',client_addr)
	WIDTH=400
	while(vid.isOpened()):
		_,frame = vid.read()
		frame = imutils.resize(frame,width=WIDTH)
		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
		message = base64.b64encode(buffer)
		server_socket.sendto(message,client_addr)
		frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
		cv2.imshow('TRANSMITINDO VÍDEO',frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			server_socket.close()
			break
		if cnt == frames_to_count:
			try:
				fps = round(frames_to_count/(time.time()-st))
				st=time.time()
				cnt=0
			except:
				pass
		cnt+=1

