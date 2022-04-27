import socket 
from funcionalidad import *
from clases import *
import threading
#inicio codigo servidor
import sys

#Variables for holding information about connections
connections = []
total_connections = 0


def ejecutivo():
    
    pass





#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    
    #funcion run es el punto de partida del objeto thread que se creo
    #esta funcion se gatilla haciendo .start()
    def run(self):
        #esta linea da una bienvenida
        self.socket.sendall(bytes("Hola! Bienvenido, Ingrese su RUT (sin guion y sin punto)", 'utf-8'))#bienvenida
        while self.signal: #mientras haya señal, recibir. Si no hay señal, entonces el cliente se ha desconectado
            try:
                #mensaje de bienvenida que se envia al cliente
                
                data = self.socket.recv(1024)
                  
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False 
                connections.remove(self)
                break
            
            if data != "" and data.decode("utf-8") != "admin":
                
                def autenticar(datas):#verifica que el rut este en la base de datos e inicializa el menu de opciones
                    datas = datas.decode('utf-8')
                    print(datas)
                    if str(datas) in dic.keys():
                        print(dic[str(datas)])
                        self.id = str(datas)  
                        ayuda(dic[str(datas)],self.socket) #inicializa el app
                        print('retorno!')
                    else:
                        self.socket.sendall(bytes("Usted no es cliente,ingrese un rut válido", 'utf-8'))
            
                autenticar(data)
                #print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)
                self.socket.close()

            if data.decode('utf-8') == "admin":                
                ejecutivo(self.socket, connections, total_connections)


                 

#esta funcion ve que clientes hay online
#Wait for new connections


def newConnections(socket):
    #esta funcion es la funcion que se le entrega al thread, establece
    #una conexion con un cliente.
    while True:
        sock, address = socket.accept() #acepta la conexion entrante
        global total_connections #variable global que cuenta las conexiones
        connections.append(Client(sock, address, total_connections, \
             "Name", True)) #connections es una lista que almacena los objetos threads
        connections[len(connections) - 1].start() #inicializa el ultimo objeto thread creado
        
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1 #actualiza el numero de conecciones activas




def main():
    #esta funcion hace dos cosas: el main se queda escuchando
    #si recibe un request inicia un thread para servirle
    
    host = '127.0.0.1'
    port = 8000

    #inicializa el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    #levanta el thread de nueva conección, el main se queda escuchando
    #se crea un objeto thread y se inicializa
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start() #inicializa el thread
    
    
main()
