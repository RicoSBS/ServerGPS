import argparse
import socket
from datetime import datetime
import requests
import json
from objdict import ObjDict

# volt = [[0,0,0],[0,0,0]]
# current = [[0,0,0],[0,0,0]]
# kwh = [[0,0,0],[0,0,0]]
# power = [[0,0,0],[0,0,0]]
# cosphi = [[0,0,0],[0,0,0]]
# frequency = [[0,0,0],[0,0,0]]
IP_server = '36.37.122.127'
Port_server = '80'
API_1 = '/sensor/EDS/Lantai_1/INCOGNITO/NE-01/'
#API_1 = '/sensor/HotelMM/test_floor/test_room/NEL-00002/'
API_2 = '/sensor/EDS/Lantai_1/INCOGNITO/NE-02/'
API = [API_1, API_2]
Token = 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlblN0YWZmIjp7Im5hbWUiOiJncmFoYXRlcmEiLCJwYXNzd29yZCI6IiQyYSQxMiRaYVNqL296MWNGOWZnYlU3MDlOREdlYlBoNGRRdGNBL01peFJXMXBMdFVyY0poSEljQXNTUyJ9LCJpYXQiOjE1NTM2NjU1Mjd9.H4ZBYpQJnpChK4RzuIOBbcJgnVJQbuN5iEfH71DLJgM'
maxbyte=1024
def_host = '127.0.0.1'
host = '0.0.0.0'

def server(port):
    indexNode = 0
    node_1 = ('192.168.100.126', port)
    node_2 = ('192.168.100.127', port)
    node = [node_1, node_2] 
    jumlahNode = len(node)
    jumlahFasa = 3
    volt = [[220.0] * jumlahFasa for i in range(jumlahNode)]
    current = [[5.0] * jumlahFasa for i in range(jumlahNode)]
    kwh = [[0.55] * jumlahFasa for i in range(jumlahNode)]
    power = [[1100.0] * jumlahFasa for i in range(jumlahNode)]
    cosphi = [[1.0] * jumlahFasa for i in range(jumlahNode)]
    frequency = [[50.0] * jumlahFasa for i in range(jumlahNode)]
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((host,port))
    pesan_balasan=('PAKET DATA SUDAH DITERIMA')
    pesan_balasan=pesan_balasan.encode('ascii')
    print('Listining at {}'.format(sock.getsockname()))
    waktu_tempo = (datetime.now()).second
    while True:
        data,address=sock.recvfrom(maxbyte)
        # print('data mentah {}'.format(data))
        # data_String=data.decode('ascii')
        Dats = data.replace(b'\00', b'')
        data_String = str(Dats, 'utf-8')
        # print(Dats)
        # print(data_String)
        for i in range(0,jumlahNode):
            if address == node[i]:
                dataJSON = json.loads(data_String)
                print('PAKET DATA DARI NODE-{}: {}'.format(i, dataJSON))
                # hitung rata-rata
                for j in range(0,jumlahFasa):
                    volt[i][j] = (volt[i][j] + float(dataJSON['volt'][i]))/2
                    volt[i][j] = round(volt[i][j],2)
                    # dataJSON.volt[i]=volt[i]
                    current[i][j] = (current[i][j] + float(dataJSON['current'][i]))/2
                    current[i][j] = round(current[i][j],2)
                    # dataJSON.current[i]=current[i]
                    kwh[i][j] = (kwh[i][j] + float(dataJSON['kwh'][i]))/2
                    kwh[i][j] = round(kwh[i][j],2)
                    # dataJSON.kwh[i]=kwh[i]
                    power[i][j] = (power[i][j] + float(dataJSON['power'][i]))/2
                    power[i][j] = round(power[i][j],2)
                    # dataJSON.power[i]=power[i]
                    cosphi[i][j] = (cosphi[i][j] + float(dataJSON['cosphi'][i]))/2
                    cosphi[i][j] = round(cosphi[i][j],2)
                    # dataJSON.cosphi[i]=cosphi[i]
                    frequency[i][j] = (frequency[i][j] + float(dataJSON['frequency'][i]))/2
                    frequency[i][j] = round(frequency[i][j],2)
                    # dataJSON.frequency[i]=frequency[i]
                # 
                break
        else:
            print('PAKET DATA DARI PENGIRIM TIDAK TERDAFTAR: DITOLAK')
        # text=data.decode('ascii')
        # print('the client at {} says {}'.format(address,text))
        sock.sendto(pesan_balasan,address)

        waktu_sekarang = datetime.now()
        # print('WAKTU SEKARANG {}'.format(waktu_sekarang.second))
        if abs(waktu_sekarang.second - waktu_tempo) >= 15:
            if(indexNode == 0): indexNode = 1
            else : indexNode = 0
            # print('kirim sesuatu ke server')
            waktu_tempo = waktu_sekarang.second
            # print('WAKTU TERAKHIR {}'.format(waktu_tempo))
            # data_String = data_String.replace("\"","\'")
            # print(data_String)
            headers =  {'Content-Type': 'application/json',
            'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlblN0YWZmIjp7Im5hbWUiOiIyMDE5LjAuMTAwIiwicGFzc3dvcmQiOiJZUFRJIiwicm9sZSI6MX0sImlhdCI6MTU2NzU5NjA5M30.eYiYtty3x9_eEX0ZA8gkYMuj8JQAQ3Cz7ENSvJga5hk',
            'Content-Length': '{}'.format(len(data_String))}
            #---------------- 
            # dataJSON = json.loads(data_String)
            # print(dataJSON)
            # kirimJSON = ObjDict()
            # kirimJSON.volt = "volt"
            # kirimJSON.current = "current"
            # kirimJSON.kwh = "kwh"
            # kirimJSON.power = "power"
            # kirimJSON.cosphi = "cosphi"
            # kirimJSON.frequency = "frequency"
            # for i in range(0, jumlahNode):
            kirimJSON = {}
            kirimJSON["volt"]=[str(volt[indexNode][0]),str(volt[indexNode][1]),str(volt[indexNode][2])]
            kirimJSON["current"]=[str(current[indexNode][0]),str(current[indexNode][1]),str(current[indexNode][2])]
            kirimJSON["kwh"]=[str(kwh[indexNode][0]),str(kwh[indexNode][1]),str(kwh[indexNode][2])]
            kirimJSON["power"]=[str(power[indexNode][0]),str(power[indexNode][1]),str(power[indexNode][2])]
            kirimJSON["cosphi"]=[str(cosphi[indexNode][0]),str(cosphi[indexNode][1]),str(cosphi[indexNode][2])]
            kirimJSON["frequency"]=[str(frequency[indexNode][0]),str(frequency[indexNode][1]),str(frequency[indexNode][2])]
            print('PAKET DATA NODE-{} KE SERVER: {}'.format(indexNode,kirimJSON))
            # kirimJSON = json.dumps(kirimJSON)
            # print(kirimJSON)
            #----------------
            SERVER = requests.post('http://'+IP_server+':'+Port_server+API[indexNode], json=kirimJSON, headers=headers)
            print(SERVER.text)
def client(port):
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    text='the time is {}'.format(datetime.now())
    data=text.encode('ascii')
    sock.sendto(data,(host,port))
    print('Client is assigned to the address {}'.format(sock.getsockname()))
    data,address=sock.recvfrom(maxbyte)
    text=data.decode('ascii')
    print('the server {} replied {}'.format(address,text))
def main():
    choices={'client':client,'server':server}
    parser=argparse.ArgumentParser(description='udp communication example')
    parser.add_argument('role',choices=choices,help='which role to play')
    parser.add_argument('-p',metavar='PORT',type=int,default=1060,help='UDP port(default 1060)')
    # parser.add_argument('-add',metavar='HOST',default=def_host,help='IP Host(default localhost)')
    args=parser.parse_args()
    function=choices[args.role]
    function(args.p)
    # function(args.add)
    
main()