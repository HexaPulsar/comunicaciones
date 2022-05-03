
from clases import *
from time import sleep
 
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


################################################################################
#####################FUNCIONALIDAD DE EJECUTIVO###################################
################################################################################
def ejecutivos(conn,connections,total_conections,self,esperando_ejecutivo,dic_clientes,dic_ejecutivos):

    def chatear(thread_ejecutivo,thread_cliente):
        s_cliente = thread_cliente.socket
        s_ejecutivo = thread_ejecutivo.socket
        #s_cliente.sendall(bytes('pruebas', 'utf-8'))
        thread_cliente.chat = True #señala si el thread esta en chat con un ejecutivo
        s_ejecutivo.sendall(bytes('ingrese ::salir para salir','utf-8'))
        while True:
            #s_ejecutivo.sendall(bytes("ingrese mensaje: ",'utf-8'))
            recibido = s_ejecutivo.recv(1024)
            if "::salir" in recibido.decode('utf-8'):
                break
            s_cliente.sendall(recibido)#le envia al cliente lo que inputeo el ejecutivo
            s_ejecutivo.sendall(s_cliente.recv(1024)) #le envia al ejecutivo lo que imputeo el cliente
            
    def atender(cliente):
        conn.sendall(bytes('Estas atendiendo a ' + cliente.nombre, 'utf-8'))
        for j in cliente.solicitudes:
            if j.state == True:
                conn.sendall(bytes('-Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: ABIERTO\n','utf-8'))
            else:
                pass #conn.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: CERRADO\n','utf-8'))
        conn.sendall(bytes("--------------------------------------------\n", "utf-8"))
        conn.sendall(bytes('\nExisten los siguientes comandos:\n|::state <abrir|cerrar>|::subject<>|::history<>|::name<>|::restart|::ver|::salir|' ,'utf-8'))
        conn.sendall(bytes('Para modificar el estado, subject, antecedentes (history), name o reiniciar servicios, ingrese el numero de solicitud seguido del comando y el nuevo input:NUMERO::COMANDO TEXTO\n','utf-8'))
        
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
                        elif comando_ejecutivo == 'abrir':
                            i.state = True
                        else:
                            conn.sendall(bytes('no es un estado valido','utf-8'))
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


    ##############INICIO INTERFAZ DE EJECUTIVO#############
                
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
        chatear(self,cliente)

    elif respuesta == '::atender':    
        for i in dic_clientes.items():
            conn.sendall(bytes("\n-------------------------------------------------\n" + i[1].nombre + ' || ' + i[1].rut + '\n', "utf-8"))
            for j in i[1].solicitudes:
                if j.state == True:
                    conn.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: ABIERTO\n','utf-8'))
                else:
                    pass#conn.sendall(bytes('Solicitud (' + str(j.ident) +'): ' + j.subject + ' || ESTADO: CERRADO\n','utf-8'))
            conn.sendall(bytes("-------------------------------------------------\n", "utf-8"))
        conn.sendall(bytes('ingrese el rut del Cliente a atender\n','utf-8'))
        cliente = conn.recv(1024).decode('utf-8')
        cliente = dic_clientes[cliente]            
        atender(cliente)
    conn.sendall(bytes('Sesión de ejecutivo terminada\n', 'utf-8'))
    return 0