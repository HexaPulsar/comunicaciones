import socket
import _thread
import sys
import http.server

#inicio codigo servidor

host = '127.0.0.1'
port = 8000



s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
 


s.listen(5)
print("waiting for connection")