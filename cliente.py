import socket
import sys
import threading
#inicio codigo cliente
#loopback server

host = '127.0.0.1'
port = 8000
 
#a continuacion se crea una funcion para recibir mensajes a través de un thread
def iniciarsocket():
    global active_thread
   
    #funcion que recibe la señal a través del socket, se paraleliza con un thread
    def receive(socket, signal):
        global active_thread
        active_thread = True
        while signal:
            #print('loop')
            #intenta recibir datos
            data = socket.recv(1024)
            print(str(data.decode("utf-8")))
            if len(data) == 0:
                active_thread = False 
                print("You have been disconnected from the server")
                break
        sys.exit(0)      
    try:#crea socket e intenta conectarse
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except:# si no se puede conectar printea que no se puede conectar
        print("Could not make a connection to the server")
        input("Press enter to quit")
        sys.exit(0)
    
    ##entra en un loop de lectura, lee lo que llega desde el servidor
    receiveThread = threading.Thread(target = receive, args = (s, True))#recieveThread almacena el objeto thread creado.
    receiveThread.start()# receiveThread.start() lo inicializa
    
    while active_thread == True: #loop para enviar mensajes a través de la conexion
        message = input()
        s.sendall(str.encode(message))
#run functions
iniciarsocket()
