import socket
 

#inicio codigo cliente
#loopback server

host = '127.0.0.1'
port = 8000


def iniciarsocket():
    global s
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((host,port)) 
        mensaje = input("message to send:")
        s.sendall(bytes(mensaje, 'utf-8')) 
        data = s.recv(1024)
        print(f"Received {data!r}") 
        
#run functions
iniciarsocket()   