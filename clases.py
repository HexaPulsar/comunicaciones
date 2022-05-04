 
import json

class Solicitud: 
    global historial
    historial = [] #lista que almacena
    def __init__(self, ident,subject, state = True):
        self.ident = ident #id de solicitud
        self.state = state #estado de la solicitud
        self.subject = subject # asunto de la solicitud
        self.antecedentes = ''
    #borra la el historial de solicitudes
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
 
class Cliente:
   #la clase cliente crea un objecto cliente. Tiene un nombre (del cliente) un rut (del cliente)
    # y el nombre del ejecutivo. Cada objecto clase tiene una lista donde se almacenan
    #las solicitudes, que a su vez son objectos de tipo solicitud
    def __init__(self,nombre,rut): 
        self.nombre= nombre #nombre del cliente
        self.rut = rut #rut del cliente
        self.solicitudes = [] #solicitudes del cliente, clase de tipo SOlicitud
        self.ejecutivo = '' #nombre del ejecutivo asociado al cliente

    def restart(self): 
        self.solicitudes = []

    def ingresar_solicitud(self,solicitud): #esta funcion ingresa en formato json las solicitudes de un cliente para armar la base de datos
         
        self.solicitudes.append(solicitud.to_json())

    def nueva_solicitud(self,solicitud):#esta funcion es en run time y agrega una nueva solicitud a la lista de solicitudes de un objeto cliente en particular.
        self.solicitudes.append(solicitud)

    def mostrar_cliente(self):
        print('nombre: ' + self.nombre)
        print('rut:  '+ self.rut) 
        print('solicitudes:  '+ str(self.solicitudes))
        print('\n\n\n')

class Ejecutivo:
    def __init__(self,nombre,rut): 
        self.nombre= nombre #nombre del ejecutivo
        self.rut = rut   #rut del ejecutivo

    def to_json(self):#esta funcion ingresa en formato json las solicitudes de un cliente para armar la base de datos
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class base:
    #una clase de base de datos para armar la base incial, no trabaja en runtime, fue solo para iniciar la base
    def __init__(self):
        self.database = {}
    
    def ingresarc(self,cliente): #ingresa un cliente a la base de datos
        #print(cliente[1])
        self.database.update({str(cliente[0]):cliente[1]}) 

    def ingresare(self,ejecutivo):#ingresa un ejecutivo a la base de datos
        self.database.update({str(ejecutivo[0]):ejecutivo[1]}) 

    def to_json(self):#esta funcion ingresa en formato json las solicitudes de un cliente para armar la base de datos
        return json.dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)