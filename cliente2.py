import socket
import sys
import threading
#inicio codigo cliente
#loopback server

host = '127.0.0.1'
port = 8000


#a continuacion se crea una funcion para recibir mensajes a través de un thread
def iniciarsocket():
    #funcion que recibe la señal a través del socket, se paraleliza con un thread
    def receive(socket, signal): 
        while signal:
            try: #intenta recibir datos
                data = socket.recv(1024)
                print(str(data.decode("utf-8"))) 
            except:# si no puede recibir datos 
                print("You have been disconnected from the server")
                signal = False
                break #termina 
    try:#crea socket e intenta conectarse
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except:# si no se puede conectar printea que no se puede conectar
        print("Could not make a connection to the server")
        input("Press enter to quit")
        sys.exit(0)

        ##entra en un loop de lectura, lee lo que llega desde el servidor
    

    #recieveThread almacena el objeto thread creado.
    # receiveThread.start() lo inicializa
    receiveThread = threading.Thread(target = receive, args = (s, True))
    receiveThread.start()

    #esta funcion es un loop para enviar mensajes a través de la conexion
    while True:
        message = input()
        s.sendall(str.encode(message))
    

#run functions
iniciarsocket()
