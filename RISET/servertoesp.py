# import socket
from socket import *
import json  
import requests 

API_ENDPOINT = "http://pastebin.com/api/api_post.php"

n=0
k=0
# bind all IP
HOST = '192.168.8.104'
# Listen on Port 
PORT = 8888 
#Size of receive buffer   
BUFFER_SIZE = 1024    
# Create a TCP/IP socket
s = socket(AF_INET, SOCK_DGRAM)
# Bind the socket to the host and port
s.bind((HOST, PORT))
# s.listen(1)

while True:
    # Receive BUFFER_SIZE bytes data
    # data is a list with 2 elements
    # first is data
    #second is client address
    n=n+1
    buf={}
    for i in range(0,2) :
        k=k+1
        data,addr = s.recvfrom(BUFFER_SIZE)
        Dats = data[0].replace(b'\00', b'')
        DatStr = str(Dats, 'utf-8')

        print(k)
        #print(Dats)
        #print(DatStr)
        JsonCvt = eval(DatStr)
        buf['Device %d'%(i)] = JsonCvt

        print("Received data from:", addr)
        if data:
            #print received data
            #print('Client to Server: ' , data)
            # Convert to upper case and send back to Client
            s.sendto(data[0].upper(), data[1])


    with open('coba.json', 'w',encoding='utf-8') as outfile:
        json.dump(buf, outfile,ensure_ascii=False,indent=4)
    k=0
    print(buf)
    print(n)
# Close connection
s.close()