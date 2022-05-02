import json
import threading
from clases import *
from time import sleep
 
c1 = Cliente("Magdalena De La Fuente","204443092")
s1 = Solicitud('01','cambio de clave wifi')
s2 = Solicitud('02','erai')
c1.agregar_solicitud(s1)
c1.agregar_solicitud(s2)


c2 = Cliente('melanie fernandez', '10101010')
ss1 = Solicitud('01','cambio de clave wifi')
ss2 = Solicitud('02','erai')
c2.agregar_solicitud(ss1)
c2.agregar_solicitud(ss2)


e1 = Ejecutivo("jesus christ",'10101010')	

#print(c1)
#print('\n\n\n')

#print(c1.solicitudes)



basec = base()
basec.ingresarc(c1)
basec.ingresarc(c2)
 

basee = base()
basee.ingresare(e1) 
 

def cerrar_base_clientes():
#cerrar json
    with open("base_clientes.json", "w") as outfile:
        outfile.write(basec.to_json())

def cerrar_base_ejecutivos():
    with open("base_ejecutivos.json", "w") as outfile:
        outfile.write(basee.to_json())

cerrar_base_clientes()
cerrar_base_ejecutivos()


def abrir_base_clientes(dic_clientes):
    def importadorc(diccionario):
            c = Cliente(diccionario['nombre'],diccionario['rut'])
            c.ejecutivo = diccionario['ejecutivo']
            c.solicitudes.append(importadors(diccionario['solicitudes']))
            #c.mostrar_cliente()
            return c

    def importadors(lista):
        
        for i in lista:
            temp = json.loads(i)
            #print(temp)
            s = Solicitud(temp['ident'],temp['subject'])
            s.state = temp['subject']
            #print(s.ident,s.subject,s.state)
            return s

    
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
