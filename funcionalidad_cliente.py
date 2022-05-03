
from clases import *
from time import sleep
 

################################################################################
#####################FUNCIONALIDAD DE CLIENTE###################################
################################################################################
def ayuda(cliente,conn,connections,esperando_ejecutivo,self): #display de ayudas
    
    print('[SERVER]: ' + cliente.nombre + " conectado")
    conn.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))
    
    #escuchar numero
    num = int(conn.recv(1024).decode('utf-8'))
    while num >4 or num <1:
        conn.sendall(bytes('elija un número válido\n','utf-8'))
        num = int(conn.recv(1024).decode('utf-8'))
    while num != 4:#loop de pregunta, si la respuesta no es 4 no sale del while
        if num == 1: 
            if len(cliente.solicitudes) == 0:
                conn.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n\nUsted no tiene solicitudes previas" + '\n', 'utf-8'))
            else:
                solicitudes = cliente.solicitudes 
                conn.sendall(bytes("Usted tiene las siguientes solicitudes en curso:\n" , 'utf-8'))
                cont = 1
                for i in solicitudes:
                    
                    if i.state == True:
                        conn.sendall(bytes(str(cont) + ') ' + str(i.subject) + '\n','utf-8'))
                        cont = cont +1
                    else:
                        continue 
                conn.sendall(bytes('\n elija una solicitud para saber más', 'utf-8'))
                solnum = conn.recv(1024).decode('utf-8')
                while int(solnum) not in [1,len(solicitudes)]:
                    conn.sendall(bytes('ese número no esta en la lista, elija otro número','utf-8'))
                    solnum = conn.recv(1024).decode('utf-8')
                
                subject = solicitudes[int(solnum)-1].antecedentes
                conn.sendall(bytes(subject, 'utf-8'))
        
        if num == 2:
            s1 = Solicitud('id','reinicio de servicios')
            s1.antecedentes = 'Su servicio no ha sido reiniciado aun, esperando a un ejecutivo\n'
            #print(type(cliente.solicitudes))
            if s1 in cliente.solicitudes:
                conn.sendall(bytes("Esta solicitud se encuentra pendiente\n ",'utf-8'))

            else:
                cliente.nueva_solicitud(s1)
                
                conn.sendall(bytes("Se ha solicitado el reinicio del servicio\n ",'utf-8'))
                print('[SERVER]:' + "Reinicio Servicios Cliente " + \
                    cliente.nombre + '.')
                #print(str(cliente.solicitudes))
        if num == 3:
            #movilizar objeto thread a una lista de espera desde la lista que guarda los threads?
            
            for i in connections: #busca el thread correspondiente en connections, luego lo cambia a la lista de threads que estan esperando un ejecutivo
                if i.name == cliente.rut:
                    esperando_ejecutivo.append(i)
                    
                    connections.remove(i)
            def chatear():
                
                conn.sendall(bytes("Estamos redirigiendo a un asistente, usted está número " + str(len(esperando_ejecutivo))+ " en la fila.",'utf-8'))
                conn.sendall(bytes('Espere a ser atendido, no se desconecte *suena musiquita de ascensor* \n','utf-8'))
                
                
                while  self.chat == False:
                    sleep(1) #espera 300 segundos antes de recordar que no se desconecte
                    #conn.sendall(bytes('Espere a ser atendido, no se desconecte *suena musiquita de ascensor* ','utf-8'))
                self.signal = False
                conn.sendall(bytes('Ejecutivo conectado!\n','utf-8'))
                

                while self.chat == True:
                    continue
            print('[SERVER]:' + ' Cliente ' + cliente.nombre + \
                ' redirijido a ejecutivo.')                            
            chatear()
        
        conn.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué más te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))
        num = int(conn.recv(1024).decode('utf-8'))
    conn.sendall(bytes("Gracias por contactarnos, que tenga un buen día!",'utf-8'))