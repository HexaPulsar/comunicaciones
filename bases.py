from clases import *

 
c1 = Cliente("Magdalena De La Fuente","204443092")
 
e1 = Ejecutivo("jesus christ",'10101010')	

s1 = Solicitud(00,'cambio de clave wifi',state = True)
s2 = Solicitud(1,'reinstalacion de OS',state = False)
s3 = Solicitud(2,'lorem ipsum',state = True)
s4 = Solicitud(3,'ayyyaya',state = False)


s1.agregar_historial('su nueva clave es \'matenme porfi\' ')
#s1.get_state()

c1.ingresar_solicitud(s1)
c1.ingresar_solicitud(s2)
c1.ingresar_solicitud(s3)
c1.ingresar_solicitud(s4)
