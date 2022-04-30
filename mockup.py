class Cliente:
    #la clase cliente crea un objecto cliente. Tiene un nombre (del cliente) un rut (del cliente)
    # y el nombre del ejecutivo. Cada objecto clase tiene una lista donde se almacenan
    #las solicitudes, que a su vez son objectos de tipo solicitud
    global solicitudes
    #ejecutivo = 'nombre ejecutivo'
    solicitudes = [Solicitud('id', self,'cambio de clave wifi',state = True),'hello','goodbye'] #lista que contendra objetos de tipo solicitud
    def __init__(self,nombre,rut,ejecutivo = ''):
        
        self.nombre= nombre
        self.rut = rut
        self.ejecutivo = ejecutivo
        
    def solicitudes_anteriores(self):
        global solicitudes
        return solicitudes

    