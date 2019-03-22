import socket
from gopigo import *


def propagator(msg, server):
    if msg == "tu":
        print("trigger up")
        stop()
    elif msg == "td":
        print("trigger down")
        fwd()
    elif "=" in msg:
        action,distance = msg.split("=")
        distance=int(distance)
        if(action == "td"):
            fwd(dist=distance)
            pulse = PPR*(distance//WHEEL_CIRC)
            while enc_read(0) < pulse:
                pass
            stop()
            server.sendMessage("st\n")
        elif action == "tl":
            turn_left_wait_for_completion(distance)
            server.sendMessage("et\n")
        elif action == "tr":
            turn_right_wait_for_completion(distance)
            server.sendMessage("et\n")
    else:
        print("Unidentified message")
        print(msg)


class tcpServer:
        
    def start(self,propagator):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("192.168.0.109",5024))
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

            self.conn.sendall(data)
        conn.close()

    def sendMessage(self,message):
        self.conn.sendall(message)


tcpServer = tcpServer()
tcpServer.start(propagator)
