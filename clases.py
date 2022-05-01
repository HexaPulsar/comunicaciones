
class Solicitud:
    historial = []
    def __init__(self, ident,subject, state = True):
        self.ident = ident #id de solicitud
        self.state = state #estado de la solicitud
        self.subject = subject # asunto de la solicitud
        
    #borra la el historial de solicitudes


        #permite ver el estado de una solicitud
    def get_state(self):
        if self.state == True:
            print('ABIERTO')
            return True
        else:
            print('CERRADO')
            return False

    def abrir(state):
        state = True

    def cerrar(state):
        state = False
    
    def agregar_historial(self,text):
        global historial
        historial.append(text)




class Cliente:
   #la clase cliente crea un objecto cliente. Tiene un nombre (del cliente) un rut (del cliente)
    # y el nombre del ejecutivo. Cada objecto clase tiene una lista donde se almacenan
    #las solicitudes, que a su vez son objectos de tipo solicitud
    def __init__(self,nombre,rut,ejecutivo = ''):
        
        self.nombre= nombre
        self.rut = rut
        self.ejecutivo = ejecutivo
        
    
    global solicitudes
    
    ejecutivo_asociado = 'nombre ejecutivo'
    solicitudes = [] #lista que contendra objetos de tipo solicitud


    def solicitudes_anteriores(self):
        global solicitudes
        return solicitudes
    
    def restart(self):
        global solicitudes
        solicitudes = []

    def ingresar_solicitud(self,solicitud):
        global solicitudes
        solicitudes.append(solicitud)
    


class Ejecutivo:
    def __init__(self,nombre,rut,ejecutivo = ''):
        
        self.nombre= nombre
        self.rut = rut
         
        