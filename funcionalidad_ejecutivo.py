
from clases import *
from time import sleep
 
#este modulo tendrá las funciones con las que interactua el cliente y con el ejecutivo en el thread


################################################################################
#####################FUNCIONALIDAD DE EJECUTIVO###################################
################################################################################
def ejecutivos(socket,connections,self,esperando_ejecutivo,dic_clientes):

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
                pass #socket.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: CERRADO\n','utf-8'))
        socket.sendall(bytes("--------------------------------------------\n", "utf-8"))
        #instrucciones de ejecutivo
        socket.sendall(bytes('\nExisten los siguientes comandos:\n|::state <abrir|cerrar>|::subject<>|::history<>|::name<>|::restart|::ver|::salir|' ,'utf-8')) 
        socket.sendall(bytes('Para modificar el estado, subject, antecedentes (history), name o reiniciar servicios, ingrese el numero de solicitud seguido del comando y el nuevo input:NUMERO::COMANDO TEXTO\n','utf-8'))
        
        comando_ejecutivo = socket.recv(1024).decode('utf-8') #comando del ejecutivo 
        
        while comando_ejecutivo:
            if "::subject" in comando_ejecutivo: #modifica el subject de una solicitud
                comando_ejecutivo.split() #elimina espacios extra en el input del ejecutivo
                solident = comando_ejecutivo[0:2] #selecciona el numero de solicitud
                comando_ejecutivo = comando_ejecutivo[2:len(comando_ejecutivo)].replace('::subject ','')#limpia el input, solo deja el input luego del comando
                comando_ejecutivo.split()
                for i in cliente.solicitudes:
                    if i.ident == solident: #busca la solicitud con ese id
                        i.subject = comando_ejecutivo #cambia el subject
                print(i.subject)

            elif '::state' in comando_ejecutivo:#modifica el estado de una solicitud
                comando_ejecutivo.split()
                solident = comando_ejecutivo[0:2] #selecciona el numero de solicitud
                
                comando_ejecutivo = comando_ejecutivo[2:len(comando_ejecutivo)].replace('::state ','') #limpia el input, solo deja el input luego del comando
                comando_ejecutivo.split()#elimina espacios extras
                for i in cliente.solicitudes:
                    if i.ident == solident:
                        if comando_ejecutivo == 'cerrar':
                            i.state = False
                        elif comando_ejecutivo == 'abrir':
                            i.state = True
                        else:
                            socket.sendall(bytes('no es un estado valido','utf-8'))
                print(i.state)
            elif "::history" in comando_ejecutivo: #modifica el historial/antecendetes de la solicitud.
                comando_ejecutivo.split()
                solident = str(comando_ejecutivo[0:2].split()) #selecciona el numero de solicitud
                comando_ejecutivo = comando_ejecutivo[2:len(comando_ejecutivo)].replace('::history ','') #limpia el input, solo deja el input luego del comando
                comando_ejecutivo.split() 
                for i in cliente.solicitudes:
                    if i.ident == solident:
                        ent = socket.recv(1024).decode('utf-8')
                        i.antecedentes = ent #edita antecedentes de la solicitud 

                print(i.antecedentes)
                
            elif "::name" in comando_ejecutivo:
                comando_ejecutivo = comando_ejecutivo[2:len(comando_ejecutivo)].replace('::name ','')
                comando_ejecutivo.split()
                cliente.ejecutivo = comando_ejecutivo
                print(cliente.ejecutivo)
            elif "::restart" in comando_ejecutivo:
                socket.sendall(bytes('se han reestablecido los servicios para el cliente\n'))
                
            elif "::salir" in comando_ejecutivo :
                break
            else:
                socket.sendall(bytes("Ese no es un comando valido, intente denuevo", 'utf-8'))
            socket.sendall(bytes('\nExisten los siguientes comandos:\n|::state <>|::subject<>|::history<>|::name<>|::restart|::salir|','utf-8'))
            comando_ejecutivo = socket.recv(1024).decode('utf-8')


    ##############INICIO INTERFAZ DE EJECUTIVO#############            
    socket.sendall(bytes('Bienvenido a la interfaz de Ejecutivo\n','utf-8'))
    socket.sendall(bytes("- hay " + str(len(connections)+ len(esperando_ejecutivo)-1) + " clientes online" + "\n", 'utf-8'))

    if len(esperando_ejecutivo) > 0:
        socket.sendall(bytes('Hay ' + str(len(esperando_ejecutivo)) + ' clientes a la espera de ser atendidos\n', 'utf-8'))
    else:
        socket.sendall(bytes('No hay clientes a la espera \n', 'utf-8'))
    #chatear o atender
    socket.sendall(bytes('Ingrese ::chatear para hablar con un cliente en espera, ingrese ::atender para visualizar las solicitudes pendientes de los clientes\n', 'utf-8'))
    respuesta = socket.recv(1024).decode('utf-8').lower()

    if respuesta == '::chatear':
        socket.sendall(bytes('Los siguientes clientes han solicitado conectarse\n','utf-8'))
        cont = 1
        for i in esperando_ejecutivo:
            socket.sendall(bytes( str(cont) + ') ' + dic_clientes[i.name].nombre + '\n', 'utf-8'))
            cont = cont +1 
        socket.sendall(bytes('ingrese el numero de cliente al que se quiere conectar\n', 'utf-8'))
        num = socket.recv(1024).decode('utf-8')
        cliente = esperando_ejecutivo[int(num)-1]
        chatear(self,cliente)

    elif respuesta == '::atender':    
        for i in dic_clientes.items():
            socket.sendall(bytes("\n-------------------------------------------------\n" + i[1].nombre + ' || ' + i[1].rut + '\n', "utf-8"))
            for j in i[1].solicitudes:
                if j.state == True:
                    socket.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: ABIERTO\n','utf-8'))
                else:
                    pass#socket.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: CERRADO\n','utf-8'))
            socket.sendall(bytes("-------------------------------------------------\n", "utf-8"))
        socket.sendall(bytes('ingrese el rut del Cliente a atender\n','utf-8'))
        cliente = socket.recv(1024).decode('utf-8')
        cliente = dic_clientes[cliente]
        atender(cliente)
    socket.sendall(bytes('Sesión de ejecutivo terminada\n', 'utf-8'))
    return 0