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
            conn.sendall(bytes("Hola! Bienvenido, Ingrese su RUT (sin guion y sin punto)", 'utf-8'))#bienvenida
            while True:
                data = conn.recv(1024) # recibe data
                if not data:
                    break #si no hay data, sale del loop
                conn.sendall(data)# TCP ECHO
                def verificar(datas,conn):#verifica que el rut este en la base de datos
                    datas = datas.decode('utf-8')
                    if str(datas) in dic.keys():
                        ayuda(dic[str(datas)],conn,s) #inicializa el app
                    else:
                        conn.sendall(bytes("Usted no es cliente,increse un rut válido", 'utf-8'))
                        s.close()
                
                verificar(data,conn) #verifica que el clientes esta en la base de datos

                ####
    ###RUN###
iniciarservidor()
