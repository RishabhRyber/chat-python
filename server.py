from socket import AF_INET,socket,SOCK_STREAM 
from threading import Thread

clients = {}
addresses = {}
HOST = ""
PORT = 33000
BUFSIZE = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

def accept_connection():
    while True:
        client,client_address = SERVER.accept()
        print(f"{client_address} has connected")
        client.send("Greetings from cave!. \n Type your name and press enter".encode('utf-8'))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(BUFSIZE).decode('utf-8')
    welcome = f"Welcome {name}! If you ever want to quit, type {'{quit}'} to exit."
    client.send(welcome.encode('utf-8'))
    msg = f"{name} has joined the chat"
    broadcast(msg.encode('utf-8'))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZE)
        if msg !=  "{quit}".encode('utf-8'):
            broadcast(msg,name+": ")
        else:
            client.send("{quit}".encode('utf-8'))
            client.close()
            del clients[client]
            broadcast(f"{name} has left the chat".encode('utf-8'))
            break

def broadcast(msg, prefix= ""):
    for sock in clients:
        sock.send(prefix.encode('utf-8')+msg)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connection)
    ACCEPT_THREAD.start()  
    ACCEPT_THREAD.join()
    SERVER.close()

