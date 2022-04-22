import socket
 

#inicio codigo cliente
#loopback server

host = '127.0.0.1'
port = 8000


def check_echo(e,r):
     
    if bytes(e,'utf-8') != (r):
        print("WARNING: CORRUPTED DATA")


def iniciarsocket():
    global s
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((host,port))
        mensaje = None
        while mensaje != "--salir":
            mensaje = input("message to send:")
            s.sendall(bytes(mensaje, 'utf-8')) 
            data = s.recv(1024)
            check_echo(mensaje,data)
        #print(f"Received {data!r}") 
        
#run functions
iniciarsocket()
   