from multiprocessing import connection
from clases import *
 
#este modulo tendrá las funciones con las que interactua el cliente y con el ejecutivo en el thread


def abrir_base_clientes(dic_clientes):
     
    def importadorc(diccionario):
            c = Cliente(diccionario['nombre'],diccionario['rut'])
            c.solicitudes = diccionario['solicitudes']
            salida = []
            c.ejecutivo = diccionario['ejecutivo']
            for i in c.solicitudes:
                temp = json.loads(i)
                s = Solicitud(temp['ident'],temp['subject'])
                s.state = temp['state']
                s.antecedentes = temp['antecedentes']
                
                salida.append(s)
            c.solicitudes = salida
            return c

    with open('base_clientes.json', 'r') as openfile:
        json_object = json.load(openfile)
         
        for i in json_object['database']:
            cliente = importadorc(i)
            dic_clientes.update({cliente.rut:cliente})

def abrir_base_ejecutivos(dic_ejecutivos):
    def importadore(diccionario):
            e = Ejecutivo(diccionario['nombre'],diccionario['rut'])
            return e

    with open('base_ejecutivos.json', 'r') as openfile:
        json_object = json.load(openfile)
        for i in json_object['database']:
            ejecutivo = importadore(i)
            dic_ejecutivos.update({ejecutivo.rut:ejecutivo})

def finalizar_sesion(dic_clientes,dic_ejecutivos):
    basec = base()
    basee = base()
    for i in dic_clientes.items():
        basec.ingresarc(i)
    for i in dic_ejecutivos.items():
        basee.ingresare(i)

    def cerrar_base_clientes(basec):
        #cerrar json
        with open("base_clientes.json", "w") as outfile:
            outfile.write(basec.to_json())

    def cerrar_base_ejecutivos(basee):
        with open("base_ejecutivos.json", "w") as outfile:
            outfile.write(basee.to_json())

    cerrar_base_clientes(basec)
    cerrar_base_ejecutivos(basee)

 
def ejecutivos(conn,connections,total_conections,self,esperando_ejecutivo,dic_clientes,dic_ejecutivos):
    conn.sendall(bytes('Bienvenido a la interfaz de Ejecutivo\n','utf-8'))
    conn.sendall(bytes("- hay " + str(len(connections)+ len(esperando_ejecutivo)-1) + " clientes online" + "\n", 'utf-8'))
     
    if len(esperando_ejecutivo) > 0:
        conn.sendall(bytes('Hay ' + str(len(esperando_ejecutivo)) + 'a la espera de ser atendidos\n', 'utf-8'))
    else:
        conn.sendall(bytes('No hay clientes a la espera \n', 'utf-8'))
    #chatear o atender
    conn.sendall(bytes('Ingrese ::chatear para hablar con un cliente en espera, ingrese ::atender para visualizar las solicitudes pendientes de los clientes\n', 'utf-8'))
    respuesta = conn.recv(1024).decode('utf-8').lower()
    if respuesta == '::chatear':
        conn.sendall(bytes('Los siguientes clientes han solicitado conectarse\n','utf-8'))
        cont = 1
        for i in esperando_ejecutivo:
            conn.sendall(bytes( str(cont) + ') ' + dic_clientes[i.name].nombre + '\n', 'utf-8'))
            cont = cont +1 
        conn.sendall(bytes('ingrese el numero de cliente al que se quiere conectar\n', 'utf-8'))
        num = conn.recv(1024).decode('utf-8')
        cliente = esperando_ejecutivo[int(num)-1]
        chatear(cliente)
    elif respuesta == '::atender':    
        for i in dic_clientes.items():
            conn.sendall(bytes("\n--------------------------------------------\n" + i[1].nombre + ' || ' + i[1].rut + '\n', "utf-8"))
            for j in i[1].solicitudes:
                if j.state == True:
                    conn.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: ABIERTO\n','utf-8'))
                else:
                    pass#conn.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: CERRADO\n','utf-8'))
            conn.sendall(bytes("--------------------------------------------\n", "utf-8"))
        conn.sendall(bytes('ingrese el rut del Cliente a atender\n','utf-8'))
        cliente = conn.recv(1024).decode('utf-8')
        cliente = dic_clientes[cliente]

        def atender(cliente):
            conn.sendall(bytes('Estas atendiendo a ' + cliente.nombre, 'utf-8'))
            for j in cliente.solicitudes:
                if j.state == True:
                    conn.sendall(bytes('-Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: ABIERTO\n','utf-8'))
                else:
                    pass#conn.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: CERRADO\n','utf-8'))
            conn.sendall(bytes("--------------------------------------------\n", "utf-8"))
            conn.sendall(bytes('\nExisten los siguientes comandos:\n|::state <>|::subject<>|::history<>|::name<>|::restart|::ver|::salir|' ,'utf-8'))
            conn.sendall(bytes('Para modificar el estado, subject, antecedentes (history), name o reiniciar servicios, ingrese el numero de solicitud seguido del comando y el nuevo input\n','utf-8'))
            conn.sendall(bytes('NUMERO::COMANDO TEXTO\n','utf-8'))
            
            comando_ejecutivo = conn.recv(1024).decode('utf-8')
            

            while comando_ejecutivo:
                if "::subject" in comando_ejecutivo:
                    comando_ejecutivo.split()
                    solident = comando_ejecutivo[0:2]
                    print(solident)
                    comando_ejecutivo = comando_ejecutivo[2:len(comando_ejecutivo)].replace('::subject ','')
                    comando_ejecutivo.split()
                    for i in cliente.solicitudes:
                        if i.ident == solident:
                            i.subject = comando_ejecutivo
                    #print(i.subject)

                elif '::state' in comando_ejecutivo:
                    comando_ejecutivo.split()
                    solident = comando_ejecutivo[0:2]
                    #print(solident)
                    comando_ejecutivo = comando_ejecutivo[2:len(comando_ejecutivo)].replace('::state ','')
                    comando_ejecutivo.split()
                    for i in cliente.solicitudes:
                        if i.ident == solident:
                            if comando_ejecutivo == 'cerrar':
                                i.state = False
                            else:
                                i.state = True
                    #print(i.state)
                elif "::history" in comando_ejecutivo:
                    comando_ejecutivo.split()
                    solident = str(comando_ejecutivo[0:2].split())
                    #print(solident)
                    comando_ejecutivo = comando_ejecutivo[2:len(comando_ejecutivo)].replace('::history ','')
                    comando_ejecutivo.split()
                    for i in cliente.solicitudes:
                        if i.ident == solident:
                            ent = conn.recv(1024).decode('utf-8')
                            i.antecedentes = ent
                    #print(i.antecedentes)
                    
                elif "::name" in comando_ejecutivo:
                    comando_ejecutivo = comando_ejecutivo[2:len(comando_ejecutivo)].replace('::name ','')
                    comando_ejecutivo.split()
                    cliente.ejecutivo = comando_ejecutivo
                    #print(cliente.ejecutivo)
                elif "::restart" in comando_ejecutivo:
                    conn.sendall(bytes('se han reestablecido los servicios para el cliente\n'))
                    
                elif "::salir" in comando_ejecutivo :
                    break 
                else:
                    conn.sendall(bytes("Ese no es un comando valido, intente denuevo", 'utf-8'))
                conn.sendall(bytes('\nExisten los siguientes comandos:\n|::state <>|::subject<>|::history<>|::name<>|::restart|::salir|','utf-8'))
                comando_ejecutivo = conn.recv(1024).decode('utf-8')
        atender(cliente)
    def chatear(thread_cliente,thread_ejecutivo):
        
        pass
    

def ayuda(cliente,conn,connections,esperando_ejecutivo): #display de ayudas
    
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
                    #print(esperando_ejecutivo)
                    connections.remove(i)
                    #print(connections)
             
            conn.sendall(bytes("Estamos redirigiendo a un asistente, usted está número " + str(len(esperando_ejecutivo))+ " en la fila.",'utf-8'))
            conn.sendall(bytes('Espere a ser atendido, no se desconecte *suena musiquita de ascensor* \n','utf-8'))
            print('[SERVER]:' + ' Cliente ' + cliente.nombre + \
                ' redirijido a ejecutivo.')
             
            #agregar un while mientras el ejecutivo este ocupado.
        
        conn.sendall(bytes("Hola" + " " + str(cliente.nombre) + \
        ", en qué más te podemos ayudar? \n \
        (1) Revisar atenciones anteriores\n \
        (2) Reiniciar servicios \n \
        (3) Contactar a un ejecutivo \n \
        (4) Salir",'utf-8'))
        num = int(conn.recv(1024).decode('utf-8'))

    conn.sendall(bytes("Gracias por contactarnos, que tenga un buen día!",'utf-8'))
    return 0 
 