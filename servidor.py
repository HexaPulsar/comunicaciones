import socket 

#inicio codigo servidor

 
host = '127.0.0.1'
port = 8000

def iniciarservidor():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    #socket.create_server(addr)
        s.bind((host,port))
        #a la espera
        print("iniciando servidor...")
        s.listen()
        conn, addr = s.accept()

        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

        print("waiting for connection")
    
iniciarservidor()
