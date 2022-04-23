
class Cliente:
    def __init__(self,nombre,rut, historial):
        self.nombre= nombre
        self.rut = rut
        self.historial = [] 


class solicitud:
    def __init__(self, subject,state,history,name,restart):
        self.subject = subject
        self.state = state ##false cerrado, True abierto
        self.history = history 
        self.name = name 
        self.restart = restart
    
 