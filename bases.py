from clases import *
#Con este script se creo la base de datos original. Es irrelevante en realidad


def abrir_base_clientes(dic_clientes):
    
    def importadorc(diccionario): #importa los objectos clientes desde la base json
             
            
            c = Cliente(diccionario['nombre'],diccionario['rut']) #crea un objecto de clase CLiente
            c.solicitudes = diccionario['solicitudes'] #asigna las solicitudes
            salida = []
             
            for i in c.solicitudes:
                s = Solicitud(i['ident'],i['subject'])
                s.state = i['state'] 
                s.antecedentes = i['antecedentes'] 
                salida.append(s)
            c.ejecutivo = diccionario['ejecutivo'] #asigna ejecutivo
            c.solicitudes = salida             
            return c
 

    with open('base_clientes.json', 'r') as openfile: #abre archivo json y gatilla llas funciones de importacion de objetos
        json_object = json.load(openfile)
        #print(json_object)
        json_object = json_object['database'].items()
        for i in json_object:
            #print(i[1])
            cliente = importadorc(i[1]) #crea un objeto cliente y lo almacena en la variable cliente
            dic_clientes.update({cliente.rut:cliente}) #agrega el cliente al diccionario
    

def abrir_base_ejecutivos(dic_ejecutivos):
    #print(dic_ejecutivos)
    def importadore(diccionario): #importa los ejecutivos en el json
            e = Ejecutivo(diccionario['nombre'],diccionario['rut'])  #crea objeto ejecutivo con elementos del diccionario entregado
            return e

    with open('base_ejecutivos.json', 'r') as openfile:
        json_object = json.load(openfile)
        json_object = json_object['database'].items()
        for i in json_object:
            ejecutivo = importadore(i[1]) #crea un objeto cliente y lo almacena en la variable cliente
            dic_ejecutivos.update({ejecutivo.rut:ejecutivo}) #agrega el cliente al diccionario
    
def finalizar_sesion(dic_clientes,dic_ejecutivos):
    #la funcion finalizar sesion guarda los datos que han sido editados hasta el momento. No se implemento en el servidor, pues este se supone que corre siempre. 
    basec = base()#crea un objeto base
    basee = base() #crea un objeto base
    for i in dic_clientes.items(): 
        basec.ingresarc(i)# ingresa a los clientes del diccionario a la base de clientes
    for i in dic_ejecutivos.items():
        basee.ingresare(i) #ingresa a los clientes del diccionario a la base de ejecutivos

    def cerrar_base_clientes(basec):
        #cerrar json
        with open("base_clientes.json", "w") as outfile:
            outfile.write(basec.to_json()) #sobreescribe el archivo json de clientes

    def cerrar_base_ejecutivos(basee):
        with open("base_ejecutivos.json", "w") as outfile:
            outfile.write(basee.to_json())#sobreescribe el archivo json de ejecutivos

            
    cerrar_base_clientes(basec)
    cerrar_base_ejecutivos(basee)
    abrir_base_clientes(dic_clientes)
    abrir_base_ejecutivos(dic_ejecutivos)
