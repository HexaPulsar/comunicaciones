import socket
import _thread
import sys
import http.server
import funcionalidad

#inicio codigo servidor

 
z    host = '127.0.0.1'
    port = 8000

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #socket.create_server(addr)
    s.bind((host,port))
    #a la espera
    s.listen(tiempodeespera)
    print("waiting for connection")
    
iniciarservidor(5)
