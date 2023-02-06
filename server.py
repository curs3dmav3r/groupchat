'Chat Room Connection - Client=To-Client'
import threading
import socket 
import sys
host = '127.0.0.1' #localhost
port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

# Functions to hanlde clients connections


def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode().startswith('REMOVE'):
                client_that_quit = msg.decode()[7:]
                quit_client(client_that_quit)
            else: 
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
                aliases.remove(alias)
                break


def quit_client(name):
    name_index = aliases.index(name)
    client_to_remove = clients[name_index]
    clients.remove(client_to_remove)
    client_to_remove.close()
    aliases.remove(name)
    print(f'{name} has quit the chat.')
    broadcast(f'{name} has quit the chat.'.encode())


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
        
        print(f'The alias of this client is {alias}.\n')
        print(f'{alias} has connected to the chat room.\n')
        broadcast(f'{alias} has connected to the chat room.\n'.encode('utf-8'))
        client.send('You are now connected!\n'.encode('utf-8'))
       
        thread = threading.Thread(target = handle_client, args=(client,))
        thread.start()


if __name__ == "__main__" :
    receive()
