 
import json
 
class Solicitud: 
    global historial
    historial = []
    def __init__(self, ident,subject, state = True):
        self.ident = ident #id de solicitud
        self.state = state #estado de la solicitud
        self.subject = subject # asunto de la solicitud
        
    #borra la el historial de solicitudes

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
     

 
class Cliente:
     
   #la clase cliente crea un objecto cliente. Tiene un nombre (del cliente) un rut (del cliente)
    # y el nombre del ejecutivo. Cada objecto clase tiene una lista donde se almacenan
    #las solicitudes, que a su vez son objectos de tipo solicitud
    def __init__(self,nombre,rut): 
        self.nombre= nombre
        self.rut = rut
        self.ejecutivo = ''
        self.solicitudes = []
        
    
    def agregar_solicitud(self,solicitud):
        self.solicitudes.append(solicitud.to_json())

    def solicitudes_anteriores(self):
         
        return self.solicitudes
    
    def restart(self): 
        self.solicitudes = []

    def ingresar_solicitud(self,solicitud):
         
        self.solicitudes.append(solicitud)
    def mostrar_cliente(self):
        print('nombre: ' + self.nombre)
        print('rut:  '+ self.rut)
        print('ejecutivo:  ' + self.ejecutivo)
        print('solicitudes:  '+ str(self.solicitudes))
        print('\n\n\n')



class Ejecutivo:

    def __init__(self,nombre,rut): 
        self.nombre= nombre
        self.rut = rut   

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class base:
    def __init__(self):
        self.database = []
    
    def ingresarc(self,cliente):
        self.database.append(cliente)
        #print(self.diccionario[str(cliente.rut)])
    def ingresare(self,ejecutivo):
        self.database.append(ejecutivo)
        #print(self.diccionario[str(cliente.rut)])
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)