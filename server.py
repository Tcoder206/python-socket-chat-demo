import threading
import socket
HOST = "127.0.0.1"
PORT = 55555
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
font = "ascii"
server.bind((HOST,PORT))
server.listen()
clients = []
nicknames = []
def broadcast(message):
	for client in clients:
		client.send(message)
def handle(client):
	while True:
		try:
			message = client.recv(1024)
			broadcast(message)
		except:
			index = clients.index(client) # gán index cho client
			clients.remove(client) # xóa client khỏi clients
			client.close() # đóng client
			nickname = nicknames[index] # nickname của client đã xóa
			broadcast(f"{nickname} left the chat".encode(font)) # gửi thông báo 
			nicknames.remove(nickname) # xóa nickname khỏi nicknames
			break
def receive():
	while True:
		client, ADDRESS = server.accept() # Cho phép địa chỉ kết nối tới server
		print(f"Connected with {str(ADDRESS)}") # Gửi địa chỉ lên server
		client.send(f"NICK".encode(font)) #
		nickname = client.recv(1024).decode(font) # Gán giá trị nickname
		clients.append(client) # Thêm client vào clients
		print(f"Nickname of the client is {nickname}") # Thông báo nickname của client
		broadcast(f"{nickname} joined the chat!".encode(font)) # Gửi thông báo
		client.send("Connected to the server".encode(font))
		thread = threading.Thread(target=handle,args=(client,))
		thread.start()
print("Server is listening...")
receive()