import socket 
from funcionalidad import *
from clases import *
import threading
from bases import c1,e1
####MUTEX SECTION


mutex = threading.Lock()
mutex.acquire()
dic_clientes = {c1.rut: c1}
#dic_clientes = {"204443092": Cliente("Magdalena De La Fuente","20.444.309-2")} #base de clientes
dic_ejecutivos = {e1.rut:e1} #base de ejecutivos

nsolicitud = 0 #trackea las solicitudes 

id_online = [] #revisar si hay un mismo rut conectado dos o mas veces

esperando_ejecutivo = [] #guarda objetos cliente

#Variables for holding information about connections
connections = [] #almacena objetos thread
total_connections = 0
online = 0 #lleva el conteo de personas que se encuentran online en el momento 
mutex.release()





#inicio codigo servidor

#cargar base de datos

def cargar():
    pass




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
        global id_online
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
            


            if data != "":
                datas = data.decode('utf-8')
                
                if str(datas) in id_online:
                    self.socket.sendall(bytes('Usted ya esta conectado en otra sesión, cierre esa sesión he intente denuevo\n','utf-8'))
                    
                    self.socket.sendall(bytes("Hola! Bienvenido, Ingrese su RUT (sin guion y sin punto)", 'utf-8'))#bienvenida
                    
                    continue
                
                if str(datas) in dic_clientes.keys() :
                    
                    id_online.append(str(datas))
                    self.id = str(datas)  
                    ayuda(dic_clientes[str(datas)],self.socket,self,id_online) #inicializa el app
                    return 
                    
                elif str(datas) in dic_ejecutivos.keys():
                    id_online.append(str(datas))
                    self.id = str(datas)  
                    ejecutivo(self.socket, connections, total_connections,self,esperando_ejecutivo)
                    return

                    
                elif "::salir" in str(datas):
                    self.socket.close()


                else:
                    self.socket.sendall(bytes("Usted no es cliente,ingrese un rut válido, ingrese \"::salir\" para salir", 'utf-8'))
                
                
                
                #print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)
                

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
        
        #print("New connection at ID " + str(connections[len(connections) - 1]))
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
