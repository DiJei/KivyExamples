import socket

class WifiUDP():
    HOST = '192.168.4.1'   # Endereco IP do Servidor
    PORT = 333             # Porta que o Servidor esta
    udp  = None
    def __init__(self):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (self.HOST, self.PORT)

    def connect(self):
            self.udp.connect(self.dest)

    def send_data(self,msg):
        data = str.encode(msg)
        self.udp.send(data)

my_socket = WifiUDP()
