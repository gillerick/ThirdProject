import time
import utime
from machine import Pin
from onewire import DS18X20
from onewire import OneWire
from network import WLAN
import socket
import urequests as requests

host= '192.168.4.112'
port = 4040

postStr ='POST / HTTP/1.1\r\n'
hostStr = 'HOST: %s:%s\r\n'%(str(host),str(port))
contentTypeStr ='Content-Type: application/json\r\n'

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == 'Upande Main':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'upande-gani#'), timeout=5000)
        while not wlan.isconnected():
            machine.idle()  # save power while waiting
        print('WLAN connection succeeded!')
        print(wlan.ifconfig()[0])
        break
#DS18B20 data line connected to pin P10
ow = OneWire(Pin('G17'))
temp = DS18X20(ow)



while True:
    temp.start_conversion()
    time.sleep(5)
    tempe =temp.read_temp_async()
    time.sleep(5)
    try:
        print("============================")
        contentStr ='{"temperature":"%.2f"}'%(tempe)
        print(contentStr)
        contentLength ='Content-Length: %s\r\n\r\n'%str(len(contentStr))
        payload = postStr+hostStr+contentTypeStr+contentLength+contentStr
        s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(payload.encode())
        svrResponse = s.recv(4096)
        s.close()
        print('sent data')
    except:
        print("passing ------------------")
        pass
    # print(payload)
    # requests.request("POST", "http://192.168.4.150:3000", '{"temperatura_rpi":' + str(500)+'}').text
