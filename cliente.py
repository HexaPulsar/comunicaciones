import socket

#inicio codigo cliente
#loopback server

host = '127.0.0.1'
port = 8000

def iniciarsocket():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((host,port)) #se conecta al servidor
        mensaje = "init"
        ##entra en un loop de lectura, lee lo que llega desde el servidor
        while True:
            data = s.recv(1024) #lee
            print(data.decode('utf-8')) #printea
            mensaje = input(' ') #ingreso de datos cliente
            s.sendall(bytes(mensaje, 'utf-8')) #envio a servidor
            s.recv(1024) #lectura de echo del servidor (por ser TCP siempre se reenvia la info al cliente)
#run functions
iniciarsocket()
