import json
import threading
from clases import *
from time import sleep
 
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

#base_inicial()


