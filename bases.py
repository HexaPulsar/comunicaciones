from clases import *

 
from clases import * 
#Con este script se creo la base de datos original. Es irrelevante en realidad
def base_inicial():
    c1 = Cliente("Magdalena De La Fuente","204443092")
    s1 = Solicitud('97','cambio de clave wifi')
    s1.antecedentes = 'tu nueva clave es JIJIJAJA'
    s2 = Solicitud('98','cancelacion de plan de datos')
    s2.antecedentes = 'mama ven a buscarme'
    c1.ingresar_solicitud(s1)
    c1.ingresar_solicitud(s2)
    c2 = Cliente('Melanie Fernandez', '10101010')
    ss1 = Solicitud('99','actualizacion de plan de internet')
    ss2 = Solicitud('100','cambio de clave wifi')
    c2.ingresar_solicitud(ss1)
    c2.ingresar_solicitud(ss2)
    e1 = Ejecutivo("NOMBRE EJECUTIVO",'00000000')	
 
    basec = base()
    basec.ingresarc(c1)
    basec.ingresarc(c2)
    basee = base()
    basee.ingresare(e1) 
    
    def cerrar_base_clientes(basec):
    #cerrar json
        with open("base_clientes.json", "w") as outfile:
            outfile.write(basec.to_json())
    def cerrar_base_ejecutivos(basee):
        with open("base_ejecutivos.json", "w") as outfile:
            outfile.write(basee.to_json())
    cerrar_base_clientes(basec)
    cerrar_base_ejecutivos(basee)
base_inicial()


def abrir_base_clientes(dic_clientes):
     
    def importadorc(diccionario): #importa los objectos clientes desde la base json
            c = Cliente(diccionario['nombre'],diccionario['rut']) #crea un objecto de clase CLiente
            c.solicitudes = diccionario['solicitudes'] #asigna las solicitudes
            salida = []
            c.ejecutivo = diccionario['ejecutivo'] #asigna ejecutivo
            for i in c.solicitudes:
                temp = json.loads(i) #carga el objeto json 
                s = Solicitud(temp['ident'],temp['subject'])# crea objeto de clase solicitud
                s.state = temp['state']#asigna estado a solicitud
                s.antecedentes = temp['antecedentes'] #asigna antecedentes a solicitud
                salida.append(s)#agrega solicitud a la lista
            c.solicitudes = salida 
            return c

    with open('base_clientes.json', 'r') as openfile: #abre archivo json y gatilla llas funciones de importacion de objetos
        json_object = json.load(openfile)
        for i in json_object['database']:
            cliente = importadorc(i) #crea un objeto cliente y lo almacena en la variable cliente
            dic_clientes.update({cliente.rut:cliente}) #agrega el cliente al diccionario

def abrir_base_ejecutivos(dic_ejecutivos):
    def importadore(diccionario): #importa los ejecutivos en el json
            e = Ejecutivo(diccionario['nombre'],diccionario['rut'])  #crea objeto ejecutivo con elementos del diccionario entregado
            return e

    with open('base_ejecutivos.json', 'r') as openfile:
        json_object = json.load(openfile) #abre archivo json
        for i in json_object['database']:
            ejecutivo = importadore(i) #importa ejecutivos
            dic_ejecutivos.update({ejecutivo.rut:ejecutivo}) #agrega objecto ejecutivo creado a un diccionario de ejecutivos

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
