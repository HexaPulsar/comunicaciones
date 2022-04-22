import socket 
from funcionalidad import *
from clases import *
#inicio codigo servidor
dic = {204443092:Cliente("magdalena de la fuente","20.444.309-2")}
 
host = '127.0.0.1'
port = 8000


    

def iniciarservidor():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    #socket.create_server(addr)
        s.bind((host,port))
        #a la espera
        print("iniciando servidor...")
        s.listen() #makes socket a listening socket
        print("Waiting for connection...")
        conn, addr = s.accept()

        with conn:
            print(f"Connected by {addr}")
            while True:
                conn.sendall("Hola! Bienvenido, Ingrese su RUT")#bienvenida
                data = conn.recv(1024)
                #print(data.decode('utf-8'))
                if not data:
                    break
                conn.sendall(data)
                def verificar(data):
                    #revisa si el rut de la persona esta en la base
                    if data in dic:
                        ayuda(dic(data))

    ###RUN###
iniciarservidor()
