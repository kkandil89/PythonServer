import socket
import sys
from _thread import *
 
class Clint:
    addr = ''
    port = 0
    conn = None 
    DeviceName = ''
   

Clintlist = [] 


host = ''
port = 8888
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket Created")

try:
    s.bind((host, port))
except socket.error:
    print("Bining Failed");
    sys.exit()

print("Socket had been bounded")

s.listen(10)

print("Socket is Ready")


def GetClientIndexByAddress(addr):
    for index,clint in enumerate(Clintlist):
        if clint.addr == addr:
            return index
    return -1 

def GetClientIndexByName(clientname):
    for index,clint in enumerate(Clintlist):
        if clint.DeviceName == clientname:
            return index
    return -1    

def clientthread(conn,addr):
    #welcomemessage = "Hello Clint"
    #conn.send(welcomemessage.encode())

    while True:
        data = conn.recv(1024)
        #reply = "OK." + data.decode() + "Add:" + addr[0]
        if not data:
            break;
        
        hexdata = []
        for byte in data:
            hexdata.append(hex(byte ))
        
        
        if hexdata[0] == hex(0x0C) and hexdata[1] == hex(0x0C) :
            if hexdata[2] == hex(0x01):
                index = GetClientIndexByAddress(addr[0])
                if index != -1:
                    name = data[3:] 
                    Clintlist[index].DeviceName = name 
                    conn.sendall(name)
                else:    
                    conn.sendall("error")
        print("data = " + data.decode() )
        #conn.sendall(data)
    conn.close()
    print("connection closed")


while 1:
    conn, addr = s.accept()
    
    c = Clint()
    c.addr = addr[0]
    c.port = addr[1]
    c.conn = conn
    c.DeviceName = ''
    Clintlist.append(c)

 
    
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    start_new_thread(clientthread, (conn,addr,))

print("connection closed")
s.close()