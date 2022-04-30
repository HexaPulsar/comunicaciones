from clases import *


base = {"204443092":Cliente("Magdalena De La Fuente","20.444.309-2"), "10101010":Cliente('Neo',"10101010")}

c1 = Cliente("Magdalena De La Fuente","20.444.309-2")

c2 = base["10101010"]




s1 = Solicitud(00,'cambio de clave wifi',state = True)



#s1.get_state()

c1.ingresar_solicitud(s1)
print(c1.solicitudes_anteriores()[0].state) 