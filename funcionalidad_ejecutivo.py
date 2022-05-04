
from bases import finalizar_sesion
from clases import *
from time import sleep
  
def ejecutivos(socket,connections,self,esperando_ejecutivo,dic_clientes,dic_ejecutivos):
    def chatear(thread_ejecutivo,thread_cliente):
        s_cliente = thread_cliente.socket #variable de socket de cliente para sintaxis mas clara
        s_ejecutivo = thread_ejecutivo.socket#variable de socket de ejecutivo para sintaxis mas clara
        #s_cliente.sendall(bytes('pruebas', 'utf-8'))
        thread_cliente.chat = True #despertamos thread cliente
        thread_cliente.esperar.set() #termina el wait del client-side
        s_ejecutivo.sendall(bytes('-------CHAT INICIADO------\n', 'utf-8'))
        s_cliente.sendall(bytes('-------CHAT INICIADO------\n', 'utf-8'))
        s_ejecutivo.sendall(bytes('Ingrese ::salir para salir\n','utf-8'))
        s_cliente.sendall(bytes('Ingrese ::salir para salir\n','utf-8'))
        while True:
            recibido_e = s_ejecutivo.recv(1024)#en primera linea del loop en caso de que el ejecutivo quiera salir sin hablar por el chat
            if "::salir" in recibido_e.decode('utf-8'):
                 #termina la espera del thread, que se pauso pues es el thread del cliente quien maneja el pin-poneo de mensajes a traves del servidor
                s_cliente.sendall(bytes('El ejecutivo se ha desconectado\n', 'utf-8'))
                s_ejecutivo.sendall(bytes('-------CHAT TERMINADO------\n', 'utf-8'))
                s_cliente.sendall(bytes('-------CHAT TERMINADO------\n', 'utf-8'))
                thread_cliente.chatear.set()
                break
            s_cliente.sendall(recibido_e)#le envia al cliente lo que inputeo el ejecutivo
            s_ejecutivo.sendall(bytes('Esperando respuesta del cliente...','utf-8'))
            recibido_c = s_cliente.recv(1024)
            if "::salir" in recibido_c.decode('utf-8'):
                s_ejecutivo.sendall(bytes('-------CHAT TERMINADO------\n', 'utf-8'))
                s_cliente.sendall(bytes('-------CHAT TERMINADO------\n', 'utf-8'))
                thread_cliente.chatear.set() #termina la espera del thread, que se pauso pues es el thread del cliente quien maneja el pin-poneo de mensajes a traves del servidor
                break
            s_ejecutivo.sendall(recibido_c) #le envia al ejecutivo lo que imputeo el cliente
            s_cliente.sendall(bytes('Esperando la respuesta del ejecutivo...', 'utf-8')) 

    def atender(cliente):
        socket.sendall(bytes('Estas atendiendo a ' + cliente.nombre, 'utf-8')) #informa al ejecutivo a que cliente se esta atendiendo
        for j in cliente.solicitudes: #se display las solicitudes activas del cliente
            if j.state == True:
                socket.sendall(bytes('-Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: ABIERTO\n','utf-8'))
            else:
                pass#socket.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: CERRADO\n','utf-8'))
        socket.sendall(bytes("--------------------------------------------\n", "utf-8"))
        
        #instrucciones de ejecutivo
        socket.sendall(bytes('\nExisten los siguientes comandos:\n|::state <abrir|cerrar>|::subject <>|::history <>|::name <>|::restart|::salir|' ,'utf-8')) 
        socket.sendall(bytes('Para modificar el estado, subject, antecedentes (history), name o reiniciar servicios, ingrese el numero de solicitud seguido del comando y el nuevo input:NUMERO::COMANDO TEXTO\n','utf-8'))
        comando_ejecutivo = socket.recv(1024).decode('utf-8') #comando del ejecutivo 
        while comando_ejecutivo:
            if "::subject" in comando_ejecutivo: #modifica el subject de una solicitud
                comando_ejecutivo.split() #elimina espacios extra en el input del ejecutivo
                cont = 0
                for i in comando_ejecutivo:#isolates solicitud number
                    if i != ':':
                        cont = cont +1
                    else:
                        solident = comando_ejecutivo[0:cont]
                        break
                    
                comando_ejecutivo = comando_ejecutivo[len(solident):len(comando_ejecutivo)].replace('::subject ','') #limpia el input, solo deja el input luego del comando
                comando_ejecutivo.split()#elimina espacios extra
                for i in cliente.solicitudes:
                    if str(i.ident) == str(solident): #busca la solicitud con ese id
                        i.subject = comando_ejecutivo #cambia el subject
                        break
            elif '::state' in comando_ejecutivo:#modifica el estado de una solicitud, funciona casi igual que ::subject
                comando_ejecutivo.split() #elimina espacios extra en el input del ejecutivo
                cont = 0
                for i in comando_ejecutivo:
                    if i != ':':
                        cont = cont +1
                    else:
                        solident = comando_ejecutivo[0:cont]
                        break 
                comando_ejecutivo = comando_ejecutivo[len(solident):len(comando_ejecutivo)].replace('::state ','') #limpia el input, solo deja el input luego del comando
                comando_ejecutivo.split() 
                for i in cliente.solicitudes:
                    if str(i.ident) == str(solident):
                         
                        if comando_ejecutivo == 'cerrar':
                            i.state = False
                            break
                            print(i.state)
                        elif comando_ejecutivo == 'abrir':
                            i.state = True
                            break
                        else:
                            socket.sendall(bytes('No es un estado valido','utf-8'))
            elif "::history" in comando_ejecutivo: #modifica el historial/antecendetes de la solicitud.
                comando_ejecutivo.split() #elimina espacios extra en el input del ejecutivo
                cont = 0
                for i in comando_ejecutivo:
                    if i != ':':
                        cont = cont +1
                    else:
                        solident = comando_ejecutivo[0:cont]
                        break   
                comando_ejecutivo = comando_ejecutivo[len(solident):len(comando_ejecutivo)].replace('::history ','') #limpia el input, solo deja el input luego del comando
                comando_ejecutivo.split() 
                for i in cliente.solicitudes:
                    if i.ident == solident:
                        ent = socket.recv(1024).decode('utf-8')
                        i.antecedentes = ent #edita antecedentes de la solicitud 
                        break
            elif "::name" in comando_ejecutivo: #cambia el nombre del ejecutivo asociado al cliente
                comando_ejecutivo.split() #elimina espacios extra en el input del ejecutivo
                cont = 0
                for i in comando_ejecutivo:
                    if i != ':':
                        cont = cont +1
                    else:
                        solident = comando_ejecutivo[0:cont]
                        break   
                comando_ejecutivo = comando_ejecutivo[len(solident):len(comando_ejecutivo)].replace('::name','') #limpia el input, solo deja el input luego del comando
                comando_ejecutivo.split() 
            elif "::restart" in comando_ejecutivo: #dummy function
                socket.sendall(bytes('Se han reestablecido los servicios para el cliente\n'))   
            elif "::salir" in comando_ejecutivo :
                break
            else:#si no es ninguno de los comandos entregados al ejecutivo
                socket.sendall(bytes("Ese no es un comando valido, intente denuevo", 'utf-8'))

            socket.sendall(bytes('\nExisten los siguientes comandos:\n|::state <>|::subject<>|::history<>|::name<>|::restart|::salir|','utf-8'))
            comando_ejecutivo = socket.recv(1024).decode('utf-8')

    ##############INICIO INTERFAZ DE EJECUTIVO#############            
    socket.sendall(bytes('Bienvenido a la interfaz de Ejecutivo\n','utf-8'))
    socket.sendall(bytes("- hay " + str(len(connections)+ len(esperando_ejecutivo)-1) + " clientes online" + "\n", 'utf-8'))

    if len(esperando_ejecutivo) > 0:#cuenta clientes esperando a un ejecutivo para chatear
        socket.sendall(bytes('Hay ' + str(len(esperando_ejecutivo)) + ' clientes a la espera de ser atendidos\n', 'utf-8'))
    else:
        socket.sendall(bytes('No hay clientes a la espera \n', 'utf-8'))
    #chatear o atender

    socket.sendall(bytes('Ingrese ::chatear para hablar con un cliente en espera, ingrese ::atender para visualizar las solicitudes pendientes de los clientes\n', 'utf-8'))
    respuesta = socket.recv(1024).decode('utf-8').lower()


    if respuesta == '::chatear':#inicializa el chat con el cliente
        socket.sendall(bytes('Los siguientes clientes han solicitado conectarse\n','utf-8'))
        cont = 1
        for i in esperando_ejecutivo:
            socket.sendall(bytes( str(cont) + ') ' + dic_clientes[i.name].nombre + '\n', 'utf-8'))
            cont = cont +1 
        socket.sendall(bytes('Ingrese el numero de cliente al que se quiere conectar\n', 'utf-8'))
        num = socket.recv(1024).decode('utf-8')
        cliente = esperando_ejecutivo[int(num)-1]
        chatear(self,cliente)

    elif respuesta == '::atender': #inicializa la opcion de visualizar a los clientes y sus solicitudes pendientes.
        cliente = ''
        while True:    
            for i in dic_clientes.items():
                socket.sendall(bytes("\n-------------------------------------------------\n" + i[1].nombre + ' || ' + i[1].rut + '\n', "utf-8"))
                for j in i[1].solicitudes:
                    if j.state == True:
                        socket.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: ABIERTO\n','utf-8'))
                    else:
                        pass#socket.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: CERRADO\n','utf-8'))
                socket.sendall(bytes("-------------------------------------------------\n", "utf-8"))
            socket.sendall(bytes('Ingrese el rut del Cliente a atender o ::salir para terminar la sesion de ejecutivo y guardar los cambios\n','utf-8'))
            cliente = socket.recv(1024).decode('utf-8')
            if "::salir" in cliente:
                break
            cliente = dic_clientes[cliente]
            atender(cliente)

    finalizar_sesion(dic_clientes,dic_ejecutivos)#guarda los cambios en la base de datos
    socket.sendall(bytes('Sesión de ejecutivo terminada\n', 'utf-8')) #mensaje de despedida para ejecutivo

    return 0