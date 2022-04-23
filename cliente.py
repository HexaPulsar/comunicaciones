import socket
import sys
import threading
#inicio codigo cliente
#loopback server

host = '127.0.0.1'
port = 8000

def iniciarsocket():
    def receive(socket, signal):
        while signal:
            try:
                data = socket.recv(1024)
                print(str(data.decode("utf-8")))
            except:
                print("You have been disconnected from the server")
                signal = False
                break
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except:
        print("Could not make a connection to the server")
        input("Press enter to quit")
        sys.exit(0)
    
        ##entra en un loop de lectura, lee lo que llega desde el servidor
    
    receiveThread = threading.Thread(target = receive, args = (s, True))
    receiveThread.start()   

    while True:
        message = input()
        s.sendall(str.encode(message))
    receiveThread.join()


#run functions
iniciarsocket()
def ignore():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((host,port)) #se conecta al servidor
        mensaje = "init"
        
        while True:
            
            data = s.recv(1024) #lee
            
            if mensaje == data:
                data = s.recv(1024)
            print(data.decode('utf-8')) #printea
            if not data:
                break
            mensaje = input(' ') #ingreso de datos cliente
            s.sendall(bytes(mensaje, 'utf-8')) #envio a servidor
            assert mensaje.encode('utf-8') == s.recv(1024)
            #s.recv(1024) #lectura de echo del servidor (por ser TCP siempre se reenvia la info al cliente)