'Chat Room Connection - Client=To-Client'
import threading
import socket 
import sys
host = '127.0.0.1' #localhost
port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = ['*']
aliases = ['*']

# Functions to hanlde clients connections


def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

#Main Function to recieve the clients connection


def receive():
    while True:
        print('Server is Running and Listening ....')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
       
        client.send(bytes('alias', 'utf-8'))
        alias = client.recv(1024).decode('utf-8')
        print(alias)
        aliases.append(alias)
        clients.append(client)
        
        print(f'The alias of this client is {alias}')
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
       
        thread = threading.Thread(target = handle_client, args=(client,))
        thread.start()


if __name__ == "__main__" :
    receive()
