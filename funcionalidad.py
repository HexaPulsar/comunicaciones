 
from clases import *

#datos para la base de datos
ejecutivo = "jesus christ"
dic = {"204443092":Cliente("Magdalena De La Fuente","20.444.309-2")}
 
#este modulo tendrá las funciones con las que interactua el cliente 



def revisar_atenciones(conn):
    conn.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n",'utf-8'))
    print('uno!')

def reiniciar_servicios(conn):
    conn.sendall(bytes("hey!",'utf-8'))
    return

def contactar_ejecutivo(conn):
    numero = ejecutivo
    conn.sendall(bytes("Estamos redirigiendo a un asistente, usted está número " + numero + " en la fila.",'utf-8'))
    

def salir(conn,s): 
    conn.sendall(bytes("Gracias por contactarnos, que tenga un buen día!",'utf-8'))
    s.shutdown()
    s.close()
    
def ayuda(cliente,conn,s): #display de ayudas
     
    print('[SERVER]: ' + cliente.nombre + " conectado")


    conn.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))
    
    #escuchar numero
    num = int(conn.recv(1024).decode('utf-8'))
    
    while num != 4:

        if num == 1: 
            revisar_atenciones(conn)
        if num == 2:
            reiniciar_servicios(conn)
            print('[SERVER]:' + "Reinicio Servicios Cliente " + \
                cliente.nombre + '.') 
        if num == 3:
            contactar_ejecutivo(conn)
            print('[SERVER]:' + ' Cliente ' + cliente.nombre + \
                ' redirijido a ejecutivo ' + ejecutivo + '.')
           


        conn.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué más te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))

        num = int(conn.recv(1024).decode('utf-8'))
    salir(conn,s)
    print('[SERVER]: ' + cliente.nombre + " descontectado.")
        