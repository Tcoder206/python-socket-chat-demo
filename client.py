import threading
import socket
HOST = "127.0.0.1"
PORT = 55555
nickname = input("Type a nickname: ")
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))
def receive():
	while True:
		try:
			message = client.recv(1024).decode("ascii")
			if message == "NICK":
				client.send(nickname.encode("ascii"))
			else:
				print(message)
		except:
			print("An error occurred!")
			client.close()
			break
def write():
	while True:
		message = f'{nickname}: {input("Type a message: ")}'
		client.send(message.encode("ascii"))
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()