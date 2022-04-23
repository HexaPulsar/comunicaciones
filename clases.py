
class Cliente:
    #la clase cliente crea un objecto cliente. Tiene un nombre (del cliente) un rut (del cliente)
    # y el nombre del ejecutivo. Cada objecto clase tiene una lista donde se almacenan
    #las solicitudes, que a su vez son objectos de tipo solicitud
    

    global solicitudes
    ejecutivo = 'nombre ejecutivo'
    def __init__(self,nombre,rut,ejecutivo = ''):
        solicitudes = []
        self.nombre= nombre
        self.rut = rut
        self.ejecutivo = ejecutivo
    
    def solicitudes_anteriores():
        global solicitudes
        return solicitudes
 


class Solicitud:
    # la clase solicitud tiene un id, un Cliente (objecto de tipo cliente), un subject o tema
    # de solicitud y un estado abierto o cerrado representado por un booleano
    
    global Cliente
    antecedentes = ' ' #almacena los antecedentes de la solicitud

    #init inicializa un objecto del tipo solicitud. cada solicitud tiene un id, un cliente
    #y un estado, que parte en True pues al crear una solicitud esta abierto
    #true para abierto, false para cerrado
    def __init__(self, ident,Cliente,subject, state = True):
        self.ident = ident 
        self.Cliente = Cliente
        self.state = state
        self.subject = subject

        
    #edit subject permite modificar el asunto relacionado con la solicitud
    def edit_subject(self):
        global Cliente
        global antecedentes
        print('\n')
        mensaje  = input('ingrese nuevo aquí: \n')
        self.subject = mensaje #modifica el subject de la solicitud
        Cliente.solicitudes.append(mensaje) # agrega la solicitud

    #get_history permite al asistente ver el historial de solicitudes anteriores
    def get_history(self):
        global Cliente
        print(Cliente.solicitudes)

    #permite cambiar el estado de una solicitud
    def change_state(self,bool):
        self.state = bool

    #permite ver el estado de una solicitud
    def get_state(self):
        if self.state == True:
            print('ABIERTO')
        else:
            print('CERRADO')
        #print(self.state)

    #permite cambiar el nombre del ejecutivo asociado
    def change_exec_name(Cliente):
        new_ejecutivo = input('nombre ejecutivo')
        Cliente.ejecutivo = new_ejecutivo
        

    #borra la el historial de solicitudes
    def restart(self):
        global Cliente
        Cliente.solicitudes = []

#permite crear una nueva solicitud 
def nueva_solicitud(ident,Cliente):
        global subject 
        subject = input('subject: \n')
        new_ejecutivo = input('nombre ejecutivo')
        Cliente.ejecutivo = new_ejecutivo
        return Solicitud(ident,Cliente,subject,state = True)


def test():
    soli = nueva_solicitud(200, Cliente('magdalena','204443092'))
    print(soli.subject)
    soli.edit_subject()
    print(soli.subject)
    soli.get_history()
    #soli.change_state(False)
    #soli.get_state()
    soli.restart()
    soli.get_history()
#test()