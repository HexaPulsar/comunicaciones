from clases import *


ejecutivo = "jesus christ"
dic = {204443092:Cliente("magdalena de la fuente","20.444.309-2")}


#este modulo tendrá las funciones con las que interactua el cliente 
def revisar_atenciones():
    print("Usted tiene las siguientes solicitudes en curso:\n")
        
    pass

def reiniciar_servicios():

    pass

def contactar_ejecutivo():
    numero = None
    print("Estamos redirigiendo a un asistente, usted está número" + numero + " en la fila.")
    pass

def salir():
    print("Gracias por contactarnos, que tenga un buen día!")
    pass
    
def ayuda(cliente): #display de ayudas
    cliente = cliente.decode('utf-8')
    print('[SERVER]' + cliente.nombre + "conectado" )
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
        print('[SERVER]:' + "Reinicio Servicios Cliente" + \
            cliente.nombre + '.')
    if num == 3:
        contactar_ejecutivo()
        print('[SERVER]:' + 'Cliente ' + cliente.nombre + \
            'redirijido a ejecutivo' + ejecutivo + '.')
    if num == 4:
        salir()
        print('[SERVER]:' + cliente.nombre + " descontectado.")