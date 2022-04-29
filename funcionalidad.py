 
from clases import *

#datos para la base de datos
ejecutivo = "jesus christ"

#aqui habrá que implementar mutex 

dic = {"204443092":Cliente("Magdalena De La Fuente","20.444.309-2")}
#print(dic['204443092'].solicitudes_anteriores())
#####

#este modulo tendrá las funciones con las que interactua el cliente 
 
def ejecutivo(conn,connections,total_conections,self):
    
    print('[SERVER]: ' + "ejecutivo" + " conectado")
    conn.sendall(bytes('Ahora tienes poderes de admin' + "\n" + "hay " + str(len(connections)-1) + " clientes online" + "\n" \
                    +   'ingrese un comando valido' + "\n", 'utf-8'))
    #conn.sendall(bytes('Los siguientes clientes han solicitado conectarse: '))
    
    
    
    conn.sendall(bytes('existen los siguientes comandos:\n\
        ' +  "|::state <>|::subject<>|::history<>|::name<>|::restart|::salir|\
            ",'utf-8'))
    
    comando_ejecutivo = conn.recv(1024).decode('utf-8')
    
    while comando_ejecutivo:
        if "::subject" in comando_ejecutivo:
            pass
        elif '::state' in comando_ejecutivo:
            pass
        elif "::history" in comando_ejecutivo:
            pass
        elif "::name" in comando_ejecutivo:
            pass
        elif "::restart" in comando_ejecutivo:
            pass
        elif "::salir" in comando_ejecutivo :
            print("[SERVER]: ejecutivo desconectado")
            self.socket.close()
            break
        elif "::refresh" in comando_ejecutivo:
            conn.sendall(bytes("hay " + str(len(connections)-1) + " clientes online" + "\n", 'utf-8'))
        else:
            conn.sendall(bytes("ese no es un comando valido, intente denuevo", 'utf-8'))
        comando_ejecutivo = conn.recv(1024).decode('utf-8')
    return    





def revisar_atenciones(conn,cliente): 
    if len(cliente.solicitudes_anteriores()) == 0:
        conn.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n \n Usted no tiene solicitudes previas" + '\n', 'utf-8'))
    else:
        solicitudes = cliente.solicitudes_anteriores()
        conn.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n" , 'utf-8'))
        cont = 1
        for i in solicitudes:
            conn.sendall(bytes(str(cont) + ') ' + str(i) + '\n','utf-8'))
            cont = cont +1
        conn.sendall(bytes("\n \n" , 'utf-8'))
        
    

def reiniciar_servicios(conn,cliente):
    #Solicitud(ident,cliente,'reinciar servicios', state = True)
    #dummy function: no hace nada excepto crear la solicitud de que se quiere
    #reiniciar las solicitudes

    conn.sendall(bytes("hey!",'utf-8'))
    return

def contactar_ejecutivo(conn):
    numero = ejecutivo
    conn.sendall(bytes("Estamos redirigiendo a un asistente, usted está número " + str(numero)+ " en la fila.",'utf-8'))
    


def ayuda(cliente,conn,self): #display de ayudas
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
            revisar_atenciones(conn,cliente)
        if num == 2:
            reiniciar_servicios(conn)
            print('[SERVER]:' + "Reinicio Servicios Cliente " + \
                cliente.nombre + '.') 
        if num == 3:
            contactar_ejecutivo(conn)
            print('[SERVER]:' + ' Cliente ' + cliente.nombre + \
                ' redirijido a ejecutivo ' + str(ejecutivo) + '.')
            #agregar un while mientras el ejecutivo este ocupado.
        #loop de pregunta
        conn.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué más te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))

        num = int(conn.recv(1024).decode('utf-8'))
  
    conn.sendall(bytes("Gracias por contactarnos, que tenga un buen día!",'utf-8'))
    print('[SERVER]: ' + cliente.nombre + " descontectado.")
    self.socket.close()
    return 0
    #return



        