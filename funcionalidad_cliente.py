
from clases import *


################################################################################
#####################FUNCIONALIDAD DE CLIENTE###################################
################################################################################
def ayuda(cliente,socket,connections,esperando_ejecutivo,thread_cliente): #display de ayudas
    print('[SERVER]: ' + cliente.nombre + " conectado")
    socket.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))
        
    num = int(socket.recv(1024).decode('utf-8'))
    while num >4 or num <1:
        socket.sendall(bytes('Elija un número válido\n','utf-8'))
        num = int(socket.recv(1024).decode('utf-8'))
    while num != 4:#loop de pregunta, si la respuesta no es 4 no sale del while
        if num == 1: 
            if len(cliente.solicitudes) == 0:
                socket.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n\nUsted no tiene solicitudes previas" + '\n', 'utf-8'))
            else:
                solicitudes = cliente.solicitudes 
                socket.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n" , 'utf-8'))
                cont = 1
                for i in solicitudes:
                    
                    if i.state == True:
                        socket.sendall(bytes(str(cont) + ') ' + str(i.subject) + '\n','utf-8'))
                        cont = cont +1
                    else:
                        continue 
                socket.sendall(bytes('\n elija una solicitud para saber más', 'utf-8'))
                solnum = socket.recv(1024).decode('utf-8')
                while int(solnum) not in [1,len(solicitudes)]:
                    socket.sendall(bytes('ese número no esta en la lista, elija otro número','utf-8'))
                    solnum = socket.recv(1024).decode('utf-8')
                subject = solicitudes[int(solnum)-1].antecedentes
                socket.sendall(bytes(subject, 'utf-8'))
        
        if num == 2:
            global n_solicitud
            s1 = Solicitud(n_solicitud,'reinicio de servicios')
            s1.antecedentes = 'Su servicio no ha sido reiniciado aun, esperando a un ejecutivo\n'
            #print(type(cliente.solicitudes))
            if s1 in cliente.solicitudes:
                socket.sendall(bytes("Esta solicitud se encuentra pendiente\n ",'utf-8'))

            else:
                cliente.nueva_solicitud(s1)
                socket.sendall(bytes("Se ha solicitado el reinicio del servicio\n ",'utf-8'))
                print('[SERVER]:' + "Reinicio Servicios Cliente " + \
                    cliente.nombre + '.')
                #print(str(cliente.solicitudes))
        if num == 3:
            #movilizar objeto thread a una lista de espera desde la lista que guarda los threads?
            for i in connections: #busca el thread correspondiente en connections, luego lo cambia a la lista de threads que estan esperando un ejecutivo
                if i.name == cliente.rut:
                    esperando_ejecutivo.append(i)
                    connections.remove(i)

            def chatear(thread_cliente):
                socket.sendall(bytes("Estamos redirigiendo a un asistente, usted está número " + str(len(esperando_ejecutivo))+ " en la fila.",'utf-8'))
                socket.sendall(bytes('Espere a ser atendido, no se desconecte *suena musiquita de ascensor* \n','utf-8'))
                thread_cliente.esperar.wait(timeout = None)
                socket.sendall(bytes('Ejecutivo conectado!\n','utf-8'))
                print('[SERVER]:' + ' Cliente ' + cliente.nombre + \
                ' redirijido a ejecutivo.')
                
                thread_cliente.chatear.wait(timeout = None)

            chatear(thread_cliente)
            esperando_ejecutivo.remove(thread_cliente)
            connections.append(thread_cliente)
        socket.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué más te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))
        num = int(socket.recv(1024).decode('utf-8'))
    socket.sendall(bytes("Gracias por contactarnos, que tenga un buen día!",'utf-8'))