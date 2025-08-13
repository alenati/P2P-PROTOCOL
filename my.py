import socket
import threading

addr = '127.0.0.1'
port1, port2 = 5000,5117
my_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)



"""host = input("wanna be host? (y/n):")
if host == 'y':
    my_sock.bind((addr,port))
    message = my_sock.recvfrom(1024)
    print(message[0])
else:
    message = input("write ur message: ")
    my_sock.sendto(message.encode(),(addr,port))"""


def recieve(my_sock,port1):
    my_sock.bind(('0.0.0.0',port1))
    while(True):
        message = my_sock.recvfrom(1024)
        print(message)

def send(my_sock,port2):
    while(True):
        message = input("type a message: ")
        if message == "e":
            break
        my_sock.sendto(message.encode(),(addr,port2))


my_port = int(input("my port:"))
other_port = int(input("friend's port:"))
threading.Thread(target = recieve,args = (my_sock,my_port),daemon = True).start()
send(my_sock,other_port)
my_sock.close()