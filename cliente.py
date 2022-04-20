import socket
import _thread
import sys
import http.server

#inicio codigo cliente
#loopback

host = '127.0.0.1'
port = 8000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket is established")
#the public ip
host = '127.0.0.1'
port = 8000
s.connect((host,port))

print("s.connect done")