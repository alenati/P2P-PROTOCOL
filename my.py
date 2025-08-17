import socket
import struct
import threading
import time

id = '127.0.0.1'
my_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
initial_seq = 100
initial_ack = 500
connection = False

SYN  = 0b00000001
ACK  = 0b00000010
KAF  = 0b00000100
FIN  = 0b00001000
DUP  = 0b00010000
NACK = 0b00100000
TXT  = 0b01000000
FRF2 = 0b10000000


class Packet:
    def __init__ (self):
        self.flag : int # 1B
        self.seq_num : int # 3B
        self.ack_num : int # 3B
        self.checksum : int # 2B
        self.data = b""  # 8B


def start_connection_init(my_sock,other_port, packet):
    if packet.flag == 0:                                #flag = None
        paketix = Packet()
        paketix.seq_num = initial_seq
        paketix.ack_num = 0
        paketix.flag = SYN
        paketix.checksum = 0
        print("[INFO] SYN sended")
        time.sleep(1)
        my_sock.sendto(new_packet(paketix), (id, other_port))
    elif packet.flag & SYN and packet.flag & ACK == 0:    #flag = SYN
        paketix = Packet()
        paketix.seq_num = packet.seq_num + 1
        paketix.ack_num = initial_ack
        paketix.flag = SYN | ACK
        paketix.checksum = 0
        time.sleep(1)
        print("[INFO] SYN-ACK sended")
        my_sock.sendto(new_packet(paketix), (id, other_port))
    elif packet.flag & SYN and packet.flag & ACK:         #flag = SYN-ACK
        paketix = Packet()
        paketix.seq_num = packet.seq_num + 1
        paketix.ack_num = packet.ack_num + 1 
        paketix.flag = ACK
        paketix.checksum = 0
        time.sleep(1)
        print("[INFO] ACK sended")
        my_sock.sendto(new_packet(paketix), (id, other_port))
        global connection
        connection = True
        return



    
     


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




def check_flag(flag):
    if flag & SYN:
        return "SYN"
    if flag & ACK:    
        print("ACK recieved")
    if flag & KAF:    
        print("KAF recieved")
    if flag & FIN:    
        print("FIN recieved")
    if flag & DUP:    
        print("DUP recieved")
    if flag & NACK:    
        print("NACK recieved")
    if flag & TXT:    
        print("TXT recieved")
    if flag & FRF2:    
        print("FRF2 recieved")
    if flag & 0b00000000:
        print("flag is NULL")




def recieve(my_sock,port, other_port):
    global connection
    my_sock.bind(('0.0.0.0',port))
    while(True):
        message, addr = my_sock.recvfrom(1024)
        paketix = unpack(message)
        #print(f"RECIEVED FLAG: {paketix.flag}, &SYN: {paketix.flag & SYN}, &ACK {paketix.flag & ACK}, &SYN-ACK {paketix.flag  & SYN and paketix.flag & ACK}")
        
        

        if paketix.flag  & SYN and paketix.flag & ACK:
            print("[INFO] SYN-ACK received")
            time.sleep(1)
            start_connection_init(my_sock,other_port, paketix)
        elif paketix.flag & SYN and paketix.flag & ACK == 0:
            
            print("[INFO] SYN recieved")
            time.sleep(1)
            start_connection_init(my_sock,other_port, paketix)
        elif paketix.flag & ACK and paketix.flag & SYN == 0:
            
            print("[INFO] ACK recieved\n[INFO] Connection established")
            connection = True

        if connection:
            if paketix.data:
                print(paketix.data.decode("utf-8"))
            continue

        
        

def send(my_sock,port, paketix = None):
    global connection
    print(f"WELL SEND FLAG!{paketix.flag}, &SYN: {paketix.flag & SYN}, &ACK {paketix.flag & ACK}, &SYN-ACK {paketix.flag  & SYN and paketix.flag & ACK}")
    while(True):
        if connection:
            if paketix == None:
                paketix = Packet()
                paketix.flag = TXT
                message = input("type a message: ")
                if message == "e":
                    break
                paketix.data = message.encode("utf-8")
        packed_data = new_packet(paketix)
        my_sock.sendto(packed_data,(id,port))






my_port = int(input("my port:"))
other_port = int(input("friend's port:"))
threading.Thread(target = recieve,args = (my_sock,my_port,other_port),daemon = True).start()
init = input("wanna initialize a connection? (y/n)") == 'y'
if init:
    paketix = Packet()
    paketix.seq_num = 0
    paketix.ack_num = 0
    paketix.flag = 0
    paketix.checksum = 0
    start_connection_init(my_sock,other_port,paketix)
else:
    print("waitin for SYN...")
        
try:
    while True:  
        time.sleep(1)
except KeyboardInterrupt:
    my_sock.close()
    print("program stopped")
#paketix = Packet()
#paketix.seq_num = 0
#paketix.ack_num = 0
#paketix.flag = 0
#paketix.checksum = 0
#send(my_sock,other_port, paketix)
my_sock.close()