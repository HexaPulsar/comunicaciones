import json
import threading
from clases import *
from time import sleep
 
c1 = Cliente("Magdalena De La Fuente","204443092")
s1 = Solicitud('01','cambio de clave wifi')
s2 = Solicitud('02','erai')

c1.agregar_solicitud(s1)
c1.agregar_solicitud(s2)
print(c1.solicitudes)

e1 = Ejecutivo("jesus christ",'10101010')	



c1 = c1.to_json()
print(c1)

print('\n')
l = json.loads(c1)
print(l)


def write():
    while True:
        with open('base.json', 'w') as f:
            json.dump(c1, f)
        #print('dumped')
        sleep(10)

threading.Thread(target=write()).start()

#dic_clientes = {c1.rut: c1}
#dic_ejecutivos = {e1.rut:e1}

 