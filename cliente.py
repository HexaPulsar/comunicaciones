import socket
import _thread
import sys
import http.server

#inicio codigo cliente
#loopback server

host = '127.0.0.1'
port = 8000


def iniciarsocket():
    global s
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket is established")

def conectar():
    
    
    #the public ip
    s.connect((host,port))

    
def desconectar():
    s.close()


def enviarmensaje():
    mensaje = input("message to send:")
    s.sendall(bytes(mensaje, 'utf-8')) 


    
#run functions
iniciarsocket()
conectar()
enviarmensaje()
desconectar()