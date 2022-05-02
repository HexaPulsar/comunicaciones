from multiprocessing.connection import wait
import socket
import threading 
from funcionalidad import *
from clases import *
from base import abrir_base_clientes, abrir_base_ejecutivos


#
print('inicializando servidor')
print('importando base...')

def cargar(): #cargar base de datos
    abrir_base_clientes(dic_clientes)
    abrir_base_ejecutivos(dic_ejecutivos)



mutex = threading.Lock()
mutex.acquire()
dic_clientes = {} #almacena objetos de tipo cliente con el rut del cliente como key
dic_ejecutivos = {}#almacena objetos de tipo ejecutivo con el rut del ejecutivo como key

nsolicitud = 0 #trackea las solicitudes 

onlinebyid = [] #revisar si hay un mismo rut conectado dos o mas veces



#Variables for holding information about connections
connections = [] #almacena objetos thread
esperando_ejecutivo = [] #aquellos threads (clientes) que estén esperando a ser conectados a un cliente se movilizan hacia esperando_ejecutivo
total_connections = 0
online = 0 #lleva el conteo de personas que se encuentran online en el momento 

mutex.release()



cargar() 
#inicio codigo servidor

class Client_thread(threading.Thread):
    global onlinebyid
    #la clase cliente facilita el desplegamiento de un thread (el thread atiende al cliente)
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket # socket
        self.address = address #direccion ip de la conexion
        self.id = id #identificador de la conexion
        self.name = name #nombre de la conexion
        self.signal = signal #señala si la conexion esta activa
        print(self.name)
    def __str__(self):
        return str(self.id) + " " + str(self.address)
     
    
    #funcion run es el punto de partida del objeto thread que se creo
    #esta funcion se gatilla haciendo .start()
    def run(self):
        #inicializa el funcionamiento del thread, corre solo por defecto, no hay que llamarla
        global onlinebyid
        global esperando_ejecutivo
        global online 
        
        if self.name in onlinebyid: #si el identificador que ingresa  el usuario  (rut) ya esta en la lista de clientes conectados
            self.socket.sendall(bytes('Usted ya esta conectado en otra sesión, cierre esa sesión he intente denuevo\n','utf-8')) #mensaje de doble sesion activa
            self.socket.sendall(bytes("Hola! Bienvenido, Ingrese su RUT (sin guion y sin punto)", 'utf-8'))# mensaje de bienvenida bienvenida
        
        while self.signal: #mientras haya señal, recibir. Si no hay señal, entonces el cliente se ha desconectado
            
            if self.name in dic_clientes.keys() : #si el identificador que ingresa el usuario  (rut) esta en el diccionario de clientes, activar la funcion de ayuda que despliega el menu
                    online = online + 1
                    onlinebyid.append(self.name)#agrega el identificador a la lista de usuarios activos
                    
                    self.id = self.name  #asigna el rut como identificador del thread
                    ayuda(dic_clientes[self.name],self.socket,self) #inicializa el app ayuda 
                     
                    onlinebyid.remove(self.name)
                    online = online -1
                    break
                    
            elif self.name in dic_ejecutivos.keys(): #si el identificador que ingreso el usuario (rut) esta en el diccionario de ejecutivos, abre el menu para ejecutivos
                online = online + 1
                onlinebyid.append(self.name)#agrega el identificador a la lista de usuarios activos
                self.id = self.name #asigna el rut como identificador del thread
                ejecutivos(self.socket, connections, total_connections,self,esperando_ejecutivo) #inicializa el app de ejecutivo
                onlinebyid.remove(self.name)
                online = online -1
                break 

            elif "::salir" in self.name: 
                self.socket.close()

            else: #si lo recibido desde el cliente no es ninguno de los anteriores se pide que reingrese un input
                self.socket.sendall(bytes("Usted no es cliente,ingrese un rut válido, ingrese \"::salir\" para salir", 'utf-8'))
                
                #print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)
                        
            try:
                #mensaje de bienvenida que se envia al cliente
                data = self.socket.recv(1024)
            except:
                #print("Client " + str(self.id) + " has disconnected")
                self.signal = False 
                connections.remove(self)
                break
            
        connections.remove(self)
        #onlinebyid.remove(self.id)
        return 0
                 

#esta funcion ve que clientes hay online
#Wait for new connections
def newConnections(socket):
    #esta funcion es la funcion que se le entrega al thread, establece
    #una conexion con un cliente.
    while True:
        sock, address = socket.accept() #acepta la conexion entrante
        global total_connections #variable global que cuenta las conexiones


        sock.sendall(bytes("Hola! Bienvenido, Ingrese su RUT (sin guion y sin punto)", 'utf-8'))
        name = str(sock.recv(1024).decode('utf-8'))
        connections.append(Client_thread(sock, address, total_connections, \
             name, True)) #connections es una lista que almacena los objetos threads
        
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crea un objeto socket
    sock.bind((host, port))
    sock.listen(5) #se queda escuchando 

    #levanta el thread de nueva conección, el main se queda escuchando
    #se crea un objeto thread y se inicializa
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,)) #crea un objecto thread
    newConnectionsThread.start() #inicializa el thread
    
     #suma a la variable que contabiliza los usuarios online
    
main()
 
 

#print('cerrando base de datos')
#cerrar_base()
#print('cerrando servidor')