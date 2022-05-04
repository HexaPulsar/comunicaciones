
import socket
import threading 

from funcionalidad_ejecutivo import *
from funcionalidad_cliente import *
from bases import *
from clases import * 
def cargar(): #cargar base de datos
    abrir_base_clientes(dic_clientes)
    abrir_base_ejecutivos(dic_ejecutivos)
mutex = threading.Lock()
mutex.acquire()
dic_clientes = {} #almacena objetos de tipo cliente con el rut del cliente como key
dic_ejecutivos = {}#almacena objetos de tipo ejecutivo con el rut del ejecutivo como key
#trackea las solicitudes 
onlinebyid = [] #revisar si hay un mismo rut conectado dos o mas veces
#Variables for holding information about connections
connections = [] #almacena objetos thread
esperando_ejecutivo = [] #aquellos threads (clientes) que estén esperando a ser conectados a un cliente se movilizan hacia esperando_ejecutivo
total_connections = 0 
mutex.release()

print('inicializando servidor')
print('importando base...')
cargar() 
print('bases importadas')
#inicio codigo servidor 
class Client_thread(threading.Thread):
    #la clase cliente facilita el desplegamiento de un thread (el thread atiende al cliente)
    global onlinebyid
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket # socket
        self.address = address #direccion ip de la conexion
        self.id = id #identificador de la conexion
        self.name = name #nombre de la conexion
        self.signal = signal #señala si la conexion esta activa
        self.esperar = threading.Event()
        self.chatear = threading.Event()
    #funcion run es el punto de partida del objeto thread que se creo
    #esta funcion se gatilla haciendo .start()
    def run(self):
        while len(self.name) != 9:
            self.socket.sendall(bytes('Largo de rut no válido, intente denuevo', 'utf-8'))
            self.name = self.socket.recv(1024).decode('utf-8') 
        #inicializa el funcionamiento del thread, corre solo por defecto, no hay que llamarla       
        if self.name in onlinebyid: #si el identificador que ingresa  el usuario  (rut) ya esta en la lista de clientes conectados
            data = self.name
            while data in onlinebyid:
                self.socket.sendall(bytes('Usted ya esta conectado en otra sesión\nCierre esa sesión he intente denuevo\nIngrese \'::salir\' para terminar la sesión \n','utf-8')) #mensaje de doble sesion activa
                self.socket.sendall(bytes("Hola! Bienvenido, Ingrese su RUT (sin guion y sin punto)", 'utf-8'))# mensaje de bienvenida bienvenida
                data = self.socket.recv(1024).decode('utf-8')
                if "::salir" in data:
                    self.socket.close()
                    connections.remove(self)
                    return 0
        while self.signal: #mientras haya señal, recibir. Si no hay señal, entonces el cliente se ha desconectado
            if self.name in dic_clientes.keys() : #si el identificador que ingresa el usuario  (rut) esta en el diccionario de clientes, activar la funcion de ayuda que despliega el menu
                    onlinebyid.append(self.name)#agrega el identificador a la lista de usuarios activos
                    self.id = self.name  #asigna el rut como identificador del thread
                    ayuda(dic_clientes[self.name],self.socket, connections,esperando_ejecutivo,self) #inicializa el app ayuda 
                    onlinebyid.remove(self.name)
                    self.socket.close()
                    print('[SERVER]: ' +  str(dic_clientes[str(self.name)].nombre) + " descontectado.")
                    break
            elif self.name in dic_ejecutivos.keys(): #si el identificador que ingreso el usuario (rut) esta en el diccionario de ejecutivos, abre el menu para ejecutivos
                onlinebyid.append(self.name)#agrega el identificador a la lista de usuarios activos
                self.id = self.name #asigna el rut como identificador del thread
                print('[SERVER]: ' + "Ejecutivo " + dic_ejecutivos[(self.name)].nombre + " conectado")
                ejecutivos(self.socket, connections,self,esperando_ejecutivo,dic_clientes) #inicializa el app de ejecutivo
                onlinebyid.remove(self.name)
                self.socket.close()
                print("[SERVER]: Ejecutivo: "   + str(dic_ejecutivos[str(self.name)].nombre) + " desconectado")
                break
            elif "::salir" in self.name: 
                self.socket.close()
            else: #si lo recibido desde el cliente no es ninguno de los anteriores se pide que reingrese un input
                self.socket.sendall(bytes("Usted no es cliente, ingrese un rut válido, ingrese \"::salir\" para salir", 'utf-8'))
        while True:
            try:
                #mensaje de bienvenida que se envia al cliente
                data = self.socket.recv(1024)
            except:
                self.signal = False #si el cliente se desconecta
                connections.remove(self)
                break
        #salida del servidor
        if self in connections: #elimina el objecto thread cuando no se esta usando más
            connections.remove(self)
        elif self in esperando_ejecutivo:
            esperando_ejecutivo.remove(self) 
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
        #inicializa un objeto thread que será identificado por el rut que se entrega en el cliente
        connections.append(Client_thread(sock, address, total_connections, \
             name, True)) #connections es una lista que almacena los objetos threads
        connections[len(connections) - 1].start() #inicializa el ultimo objeto thread creado
        total_connections += 1 #actualiza el numero de conecciones activas

def main():
    #esta funcion hace dos cosas: el main se queda escuchando
    #si recibe un request inicia un thread para servirle
    host = '127.0.0.1'
    port = 8000
    #inicializa el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crea un objeto socket
    sock.bind((host, port))
    sock.listen() #se queda escuchando 
    #levanta el thread de nueva conección, el main se queda escuchando
    #se crea un objeto thread y se inicializa
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,)) #crea un objecto thread
    newConnectionsThread.start() #inicializa el thread
main()
#print('cerrando base de datos')
#cerrar_base()
#print('cerrando servidor')