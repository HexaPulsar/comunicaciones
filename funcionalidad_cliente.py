
from clases import *


################################################################################
#####################FUNCIONALIDAD DE CLIENTE###################################
################################################################################
def ayuda(cliente,socket,connections,esperando_ejecutivo,thread_cliente): #permite la funcionalidad de ayudar all cliente

    print('[SERVER]: ' + cliente.nombre + " conectado") #log de consola servidor
    #mensaje de bienvenida, se envia al cliente
    socket.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))
        
    num = int(socket.recv(1024).decode('utf-8')) #se recibe la respuesta de selección de menu por parte del cliente
    while num >4 or num <1:#si el numero no es entre 1 y 4 preguntar hasta que lo sea
        socket.sendall(bytes('Elija un número válido\n','utf-8'))
        num = int(socket.recv(1024).decode('utf-8'))
    while num != 4:#loop de pregunta, si la respuesta no es 4 no sale del while
        if num == 1: 
            if len(cliente.solicitudes) == 0:# si no hay solicitudes
                socket.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n\nUsted no tiene solicitudes previas" + '\n', 'utf-8'))
            else:
                #printea una lista con las solicitudes activas
                solicitudes = cliente.solicitudes 
                socket.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n" , 'utf-8'))
                cont = 1
                for i in solicitudes:
                    
                    if i.state == True:
                        socket.sendall(bytes(str(cont) + ') ' + str(i.subject)+ '\n','utf-8'))
                        cont = cont +1
                    else:
                        continue
                    
                socket.sendall(bytes('\nElija una solicitud para saber más', 'utf-8')) #detalle de una solicitud activa
                solnum = socket.recv(1024).decode('utf-8')
                while int(solnum) not in [1,len(solicitudes)]:#si el numero no esta en la lista preguntar hasta que esté
                    socket.sendall(bytes('ese número no esta en la lista, elija otro número','utf-8'))
                    solnum = socket.recv(1024).decode('utf-8')
                subject = solicitudes[int(solnum)-1].antecedentes
                socket.sendall(bytes(subject, 'utf-8'))
        if num == 2:#genera una solicitud automática de reinicio de servicios que se agrega a la lista de solicitudes pendientes del cliente.
            def buscar(listasolicitudes):
                bool = False
                for i in listasolicitudes:
                    if i.subject == 'Reinicio de servicios':
                        bool = True #esta en 
                        break
                return bool
            
            if buscar(cliente.solicitudes) != True: #si la solicitud ya existe, reactivarla, si no existe, crearla.                       
                n_solicitud =  int(cliente.solicitudes[-1].ident) + 1
                s1 = Solicitud(str(n_solicitud),'Reinicio de servicios')
                s1.antecedentes = 'Su servicio no ha sido reiniciado aun, esperando a un ejecutivo\n'
                #print(type(cliente.solicitudes))
                if s1 in cliente.solicitudes:
                    socket.sendall(bytes("Esta solicitud se encuentra pendiente\n ",'utf-8'))
                else:
                    cliente.nueva_solicitud(s1)
                    socket.sendall(bytes("Se ha solicitado el reinicio del servicio\n",'utf-8'))
                    print('[SERVER]:' + "Reinicio Servicios Cliente " + cliente.nombre + '.')
                    #print(str(cliente.solicitudes))
            else:
                for i in cliente.solicitudes:
                    if i.subject == 'Reinicio de servicios':
                        i.state = True #esta en 
                        break
        if num == 3:#
            #movilizar objeto thread a una lista de espera desde la lista que guarda los threads?
            for i in connections: #busca el thread correspondiente en connections, luego lo cambia a la lista de threads que estan esperando un ejecutivo
                if i.name == cliente.rut:
                    esperando_ejecutivo.append(i)
                    connections.remove(i)

            def chatear(thread_cliente):#inicializa la suspension temporal del thread mientras se conecta un ejecutivo.
                socket.sendall(bytes("Estamos redirigiendo a un asistente, usted está número " + str(len(esperando_ejecutivo))+ " en la fila.",'utf-8'))
                socket.sendall(bytes('Espere a ser atendido, no se desconecte *suena musiquita de ascensor* \n','utf-8'))
                thread_cliente.esperar.wait(timeout = None) #evento que suspende el thread. espera indefinidamente.
                socket.sendall(bytes('Ejecutivo conectado!\n','utf-8'))
                print('[SERVER]:' + ' Cliente ' + cliente.nombre + \
                ' redirijido a ejecutivo.')#logeo de consola
                thread_cliente.chatear.wait(timeout = None) #suspende el thread hasta que el ejecutivo se desconecte
            chatear(thread_cliente)
            esperando_ejecutivo.remove(thread_cliente)#saca al objeto cliente_thread de la lista de clientes esperando un ejecutivo para el chat
            connections.append(thread_cliente)
        #re-despliege de menu del cliente.    
        socket.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué más te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))
        num = int(socket.recv(1024).decode('utf-8'))
    socket.sendall(bytes("Gracias por contactarnos, que tenga un buen día!",'utf-8'))#despedida si num == 4