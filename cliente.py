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
    

#run functions
iniciarsocket()
