import threading 
import socket
import sys
alias = input('Choose an alias >>>')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'alias':
                client.send(bytes(alias,'utf-8'))
            
            elif('You are now connected!' in message):
                b = message[-22:]
                c = message[0:-22]
                print(c)
                print(b)
            else:
                print(message)
                
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()