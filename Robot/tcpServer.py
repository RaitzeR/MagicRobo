import socket

class tcpServer:
    def __init__(self):
        self.start()
        
    def start(self,propagator):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("192.168.0.112",5024))
        s.listen(1)
        print("Server started, waiting for connections")
        conn, addr = s.accept()
        self.conn = conn
        print("accepted connection")
        while 1:
            data = conn.recv(1024)
            if not data:
                break
            for message in data.decode().split("\n")[:-1]:
                propagator(message, self)

            conn.sendall(data)
        conn.close()

    def sendMessage(message):
        conn.sendall(message)
