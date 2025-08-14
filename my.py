import socket
import struct
import threading

id = '127.0.0.1'
my_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


class Packet:
    def __init__ (self):
        self.flag : int # 1B
        self.seq_num : int # 3B
        self.ack_num : int # 3B
        self.checksum : int # 2B
        self.data = b""  # 8B


def new_packet(packet):
    header = struct.pack(
        "!BIIH",
        packet.flag,
        packet.seq_num,
        packet.ack_num,
        packet.checksum,
        
    )
    header += packet.data
    return header

def unpack(packed_data):
    header_size = struct.calcsize("!BIIH")
    flag, seq_num, ack_num, checksum = struct.unpack("!BIIH", packed_data[:header_size])
    packet = Packet()
    packet.flag = flag
    packet.seq_num = seq_num
    packet.ack_num = ack_num
    packet.checksum = checksum
    packet.data = packed_data[header_size:]
    return packet



"""host = input("wanna be host? (y/n):")
if host == 'y':
    my_sock.bind((addr,port))
    message = my_sock.recvfrom(1024)
    print(message[0])
else:
    message = input("write ur message: ")
    my_sock.sendto(message.encode(),(addr,port))"""


SYN  = 0b00000001
ACK  = 0b00000010
KAF  = 0b00000100
FIN  = 0b00001000
DUP  = 0b00010000
NACK = 0b00100000
TXT  = 0b01000000
FRF2 = 0b10000000

def check_flag(flag):
    if flag & SYN:
        print("SYN sended")
    if flag & ACK:    
        print("ACK sended")
    if flag & KAF:    
        print("KAF sended")
    if flag & FIN:    
        print("FIN sended")
    if flag & DUP:    
        print("DUP sended")
    if flag & NACK:    
        print("NACK sended")
    if flag & TXT:    
        print("TXT sended")
    if flag & FRF2:    
        print("FRF2 sended")
    if flag & 0b00000000:
        print("flag is NULL")




def recieve(my_sock,port):
    my_sock.bind(('0.0.0.0',port))
    while(True):
        message, addr = my_sock.recvfrom(1024)
        paketix = unpack(message)
        print(paketix.data.decode("utf-8"))

def send(my_sock,port, paketix):
    while(True):
        message = input("type a message: ")
        if message == "e":
            break
        paketix.data = message.encode("utf-8")
        packed_data = new_packet(paketix)
        my_sock.sendto(packed_data,(id,port))

paketix = Packet()
paketix.seq_num = 100
paketix.ack_num = 100
paketix.flag = ACK
paketix.checksum = 69


my_port = int(input("my port:"))
other_port = int(input("friend's port:"))
threading.Thread(target = recieve,args = (my_sock,my_port),daemon = True).start()
send(my_sock,other_port, paketix)
my_sock.close()