# import socket

# HOST = '192.168.2.5'
# PORT = 7777
# BUFFER_SIZE = 1024

# def upload_video(filename):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         s.send(f"upload,{filename}".encode())

#         with open(filename, 'rb') as f:
#             for line in f:
#                 s.send(line)

#         s.send(b'DONE')

# def list_videos():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         s.send("list,".encode())
#         data = s.recv(BUFFER_SIZE)
#         print(data.decode())

# def download_video(filename):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         s.send(f"download,{filename}".encode())

#         with open(filename, 'wb') as f:
#             while True:
#                 file_data = s.recv(BUFFER_SIZE)
#                 if not file_data:
#                     break
#                 f.write(file_data)

# # Exemplo
# # upload_video("video1.mp4")
# list_videos()
# download_video("video1.mp4")

################################################################################################################################################


# This is client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = 'localhost'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9999
message = b'Hello'

client_socket.sendto(message,(host_ip,port))
fps,st,frames_to_count,cnt = (0,0,20,0)
while True:
	packet,_ = client_socket.recvfrom(BUFF_SIZE)
	data = base64.b64decode(packet,' /')
	npdata = np.fromstring(data,dtype=np.uint8)
	frame = cv2.imdecode(npdata,1)
	frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
	cv2.imshow("RECEBENDO VÍDEO",frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		client_socket.close()
		break
	if cnt == frames_to_count:
		try:
			fps = round(frames_to_count/(time.time()-st))
			st=time.time()
			cnt=0
		except:
			pass
	cnt+=1

