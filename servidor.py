import socket 
from funcionalidad import *
from clases import *
import threading

####MUTEX SECTION







#inicio codigo servidor
 
#Variables for holding information about connections
connections = []
total_connections = 0
online = 0 #lleva el conteo de personas que se encuentran online en el momento 
id_online = [] #revisar si hay un mismo rut conectado dos o mas veces

esperando_ejecutivo = [] #guarda objetos cliente
 
 
class Client_thread(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
     
    
    #funcion run es el punto de partida del objeto thread que se creo
    #esta funcion se gatilla haciendo .start()
    def run(self):
        global esperando_ejecutivo
        #esta linea da una bienvenida
        self.socket.sendall(bytes("Hola! Bienvenido, Ingrese su RUT (sin guion y sin punto)", 'utf-8'))#bienvenida
        while self.signal: #mientras haya señal, recibir. Si no hay señal, entonces el cliente se ha desconectado
            try:
                #mensaje de bienvenida que se envia al cliente
                
                data = self.socket.recv(1024)
                  
            except:
                #print("Client " + str(self.id) + " has disconnected")
                self.signal = False 
                connections.remove(self)
                break
            
            if data != "" and data.decode("utf-8") != "admin":
                datas = data.decode('utf-8')
                
                if str(datas) in id_online:
                    self.socket.sendall(bytes('Usted ya esta conectado en otra sesión','utf-8'))
                if str(datas) in dic.keys() :
                    
                    id_online.append(str(datas))
                    self.id = str(datas)  
                    ayuda(dic[str(datas)],self.socket,self) #inicializa el app
                    return 
                elif str(datas) == "::salir":
                    return
                else:
                    self.socket.sendall(bytes("Usted no es cliente,ingrese un rut válido, ingrese \"::salir\" para salir", 'utf-8'))
                #print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)
                

            if data.decode('utf-8') == "admin":                
                ejecutivo(self.socket, connections, total_connections,self,esperando_ejecutivo)
                break

        global online
        online = online -1
        #id_online.remove(self.id)
        return 0
                 

#esta funcion ve que clientes hay online
#Wait for new connections





def newConnections(socket):
    #esta funcion es la funcion que se le entrega al thread, establece
    #una conexion con un cliente.
    while True:
        sock, address = socket.accept() #acepta la conexion entrante
        global total_connections #variable global que cuenta las conexiones
        connections.append(Client_thread(sock, address, total_connections, \
             "Name", True)) #connections es una lista que almacena los objetos threads
        connections[len(connections) - 1].start() #inicializa el ultimo objeto thread creado
        
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1 #actualiza el numero de conecciones activas


def main():
    #esta funcion hace dos cosas: el main se queda escuchando
    #si recibe un request inicia un thread para servirle
    global online
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
    online = online + 1
    
main()
