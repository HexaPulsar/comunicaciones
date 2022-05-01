import json
class Solicitud: 
    global historial
    historial = []
    def __init__(self, ident,subject, state = True):
        self.ident = ident #id de solicitud
        self.state = state #estado de la solicitud
        self.subject = subject # asunto de la solicitud
        
    #borra la el historial de solicitudes

    def __iter__(self):
        global historial
        yield from {
            "ident": self.ident,
            "state": self.state,
            "subject": self.subject,
            "historial" : str(historial),
        }.items()


    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def to_json(self):
        return self.__str__()
    



class Cliente:
     
   #la clase cliente crea un objecto cliente. Tiene un nombre (del cliente) un rut (del cliente)
    # y el nombre del ejecutivo. Cada objecto clase tiene una lista donde se almacenan
    #las solicitudes, que a su vez son objectos de tipo solicitud
    def __init__(self,nombre,rut): 
        self.nombre= nombre
        self.rut = rut
        self.ejecutivo = ''
        self.solicitudes = []
          

    def __iter__(self):  
        yield from {
            "nombre": self.nombre,
            "rut": self.rut,
            "ejecutivo": self.ejecutivo,
            "solicitudes" : self.solicitudes,
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def to_json(self):
        return self.__str__()
    
    def agregar_solicitud(self,solicitud):
        self.solicitudes.append(solicitud.to_json())

    def solicitudes_anteriores(self):
         
        return self.solicitudes
    
    def restart(self): 
        self.solicitudes = []

    def ingresar_solicitud(self,solicitud):
         
        self.solicitudes.append(solicitud)
    
class Ejecutivo:

    def __init__(self,nombre,rut): 
        self.nombre= nombre
        self.rut = rut   

    def __iter__(self):  
        yield from {
            "nombre": self.nombre,
            "rut": self.rut,
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def to_json(self):
        return self.__str__()