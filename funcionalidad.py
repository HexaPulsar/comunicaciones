#este modulo tendrá las funciones con las que interactua el cliente 
def revisar_atenciones():
    pass

def reiniciar_servicios():
    pass

def contactar_ejecutivo():
    pass

def salir():
    pass

def ayuda(cliente): #display de ayudas
    print("Hola" + " " + str(cliente.nombre) + \
        ", en qué te podemos ayudar?")
    
    print("(1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir")
    num = input(' ')

    if num == 1:
        revisar_atenciones()
    if num == 2:
        reiniciar_servicios()
    if num == 3:
        contactar_ejecutivo()
    if num == 4:
        salir()