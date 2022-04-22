import socket 
from funcionalidad import *
from clases import *
#inicio codigo servidor
 
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
                conn.sendall(bytes("Hola! Bienvenido, Ingrese su RUT (sin guion y sin punto)", 'utf-8'))#bienvenida
                data = conn.recv(1024)
                print(data.decode('utf-8'))
                if not data:
                    break
                conn.sendall(data)
                def verificar(datas):
                    #revisa si el rut de la persona esta en la base

                    ###arreglar data###
                    if int(datas) in dic:
                        ayuda(dic[str(datas)])
                    else:
                        print("usted no es cliente")
                       
                verificar(data)
                ####
    ###RUN###
iniciarservidor()
